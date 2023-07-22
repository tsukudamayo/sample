import argparse
import base64
import os
import pprint
import sys
import time
from typing import List, Tuple, Dict

import hvac
import psycopg2
import pyotp
import requests

from totp import create_totp_key, enable_totp_secrets_engine, read_totp_code, veriry_totp_code
from nortification import send_email


havc_client = {
    "url": os.environ["VAULT_ADDR"]
}
psql_host = os.environ["POSTGRES_URL"]
root_username = os.environ["ROOT_USERNAME"]
root_password = os.environ["ROOT_PASSWORD"]
db_name = "postgres"

root_payload = {
    "plugin_name": "postgresql-database-plugin",
    "connection_url": "postgresql://" + root_username + ":" + root_password + "@" + psql_host + "/postgres?sslmode=disable",
    "allowed_roles": [ "readonly", "admin"],
    "username": root_username,
    "password": root_password,
}

readonly_payload = {
    "db_name": "postgresql",
    "creation_statements": [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}' INHERIT;",
    "GRANT ro TO \"{{name}}\";"
  ],
    "default_ttl": "1m",
    "max_ttl": "2m"
}

transit_policy = """
# Enable transit secrets engine
path "sys/mounts/transit" {
  capabilities = [ "create", "read", "update", "delete", "list" ]
}

# To read enabled secrets engines
path "sys/mounts" {
  capabilities = [ "read" ]
}

# Manage the transit secrets engine
path "transit/*" {
  capabilities = [ "create", "read", "update", "delete", "list" ]
}

path "transit/encrypt/*" {
   capabilities = [ "update" ]
}

path "transit/decrypt/*" {
   capabilities = [ "update" ]
}
"""

admin_policy = """
# Mount secrets engines
path "sys/mounts/*" {
  capabilities = [ "create", "read", "update", "delete", "list" ]
}

# Configure the database secrets engine and create roles
path "database/*" {
  capabilities = [ "create", "read", "update", "delete", "list" ]
}

# Manage the leases
path "sys/leases/+/database/creds/readonly/*" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}

path "sys/leases/+/database/creds/readonly" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}

# Write ACL policies
path "sys/policies/acl/*" {
  capabilities = [ "create", "read", "update", "delete", "list" ]
}

# Manage tokens for verification
path "auth/token/create" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}
"""

apps_policy = """
# Get credentials from the database secrets engine 'readonly' role.
path "database/creds/readonly" {
  capabilities = [ "read" ]
}
"""


# encrypt userpass
def transit_encrypt(
    client: hvac.Client,
    plain_text: str,
    encrypt_key: str,
):
    encoded_text = base64.b64encode(plain_text.encode("utf-8"))
    # print("encoded_text", encoded_text)
    # print("encrypt_key : ", encrypt_key)
    cipher_text = client.secrets.transit.encrypt_data(
        name=encrypt_key,
        plaintext=str(encoded_text, "utf-8"),
    )

    return cipher_text["data"]["ciphertext"]


# decrypt userpass
def transit_decrypt(
    client: hvac.Client,
    ciphertext: str,
    decrypt_key: str,
):
    decrypt_data_response = client.secrets.transit.decrypt_data(
        name=decrypt_key,
        ciphertext=ciphertext,
    )

    return str(base64.b64decode(decrypt_data_response["data"]["plaintext"]), "utf-8")


def psql_connection(
    client: hvac.Client,
    role: str,
):
    if role == "admin":
        _payload = {
            "db_name": "postgresql",
            "creation_statements": [
                "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}' INHERIT;",
                "GRANT root TO \"{{name}}\";"
            ],
            "default_ttl": "1m",
            "max_ttl": "2m"
        }
        # create users table
        create_users_table_if_not_exist(config=root_payload)
    elif role == "readonly":
        _payload = {
            "db_name": "postgresql",
            "creation_statements": [
                "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}' INHERIT;",
                "GRANT ro TO \"{{name}}\";"
            ],
            "default_ttl": "1m",
            "max_ttl": "2m"
        }
    else:
        raise ValueError(f"role: {role} does not exist")

    # create role
    response = create_database_role(
        client=client,
        name=role,
        mount_point="database",
        config=_payload,
    )
    # print(response)
    # print(type(response))

    response = verify_database_role(
        client=client,
        role_name=role,
    )
    # pprint.pprint(response)
    psql_creds = client.secrets.database.generate_credentials(name=role)
    # print("psql_creds")
    # pprint.pprint(psql_creds)
    db_name="postgres"
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database=db_name,
        user=psql_creds["data"]["username"],
        password=psql_creds["data"]["password"]
    )

    return connection


def psql_input(
    sql_statement: str,
    username: str,
    ciphertext,
    connection,
) -> None:
    cursor = connection.cursor()
    cursor.execute(sql_statement, (username, ciphertext))

    connection.commit()

    return None


def psql_retrieval(
    sql_statement: str,
    username: str,
    connection,
) -> List[Tuple]:
    cursor = connection.cursor()
    cursor.execute(
        sql_statement,
        (username,),
    )
    records = cursor.fetchall()

    return records


def enable_database_secrets_engine(
    client: hvac.Client,
    config: Dict[str, str],
    path: str,
) -> requests.models.Response:
    return client.sys.enable_secrets_engine(
        backend_type="database",
        path=path,
        config=config,
    )


def configure_database_secrets_engine(
    client: hvac.Client,
    name: str,
    config: Dict[str, str],
    
) -> requests.models.Response:
    return client.secrets.database.configure(
        name="postgresql",
        plugin_name=config["plugin_name"],
        connection_url=config["connection_url"],
        allowed_roles=config["allowed_roles"],
        username=config["username"],
        password=config["password"],
    )


def create_database_role(
    client: hvac.Client,
    name: str,
    mount_point: str,
    config: Dict[str, str],
) -> requests.models.Response:
    return client.write(
        path="/database/roles/" + name,
        db_name=config["db_name"],
        creation_statements=config["creation_statements"],
        default_ttl=config["default_ttl"],
        max_ttl=config["max_ttl"],
        mount_point=mount_point,
    )


def verify_database_role(
    client: hvac.Client,
    role_name: str,
) -> None:
    return client.read("/database/roles/" + role_name)


def enable_transit_secrets_engine(
    client: hvac.Client,
    path: str,
) -> requests.models.Response:
    return client.sys.enable_secrets_engine(
        backend_type="transit",
        path=path,
    )


def enable_userpass_auth_method(
    client: hvac.Client,
    path: str,
) -> requests.models.Response:
    return client.sys.enable_auth_method(
        method_type="userpass",
        path=path,
    )


def create_users_table_if_not_exist(config: Dict) -> None:
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user=config["username"],
        password=config["password"]
    )
    cursor = connection.cursor()
    cursor.execute("""
create table if not exists users (
    username varchar(255),
    password varchar(255)
)
"""
    )
    connection.commit()
    connection.close()
    cursor.close()

    return None


def main():
    client: hvac.Client = hvac.Client(**havc_client)
    # print(client)
    # print(type(client))
    assert client.is_authenticated()

    ############
    # postgres #
    ############
    # enable secrets engine
    mount_path = "database"
    mounted_path = client.sys.list_mounted_secrets_engines()
    # pprint.pprint(mounted_path)
    # print(type(mounted_path))
    if mount_path + "/" not in mounted_path:
        response = enable_database_secrets_engine(
            client=client,
            config=root_payload,
            path=mount_path,
        )
        # print(response)
        # print(type(response))

    # configure postgresql plugin for connecting credentials
    response = configure_database_secrets_engine(
        client=client,
        name="database",
        config=root_payload,
    )
    # print(response)

    ###########
    # transit #
    ###########
    # create policy
    response = client.sys.create_or_update_policy(
        name='transit-writer',
        policy=transit_policy,
    )
    # print(response)

    response = client.sys.create_or_update_policy(
        name='admin',
        policy=admin_policy,
    )
    # print(response)

    response = client.sys.create_or_update_policy(
        name='apps',
        policy=apps_policy,
    )
    # print(response)

    # enable secrets engine
    mount_path = "transit"
    mounted_path = client.sys.list_mounted_secrets_engines()
    # pprint.pprint(mounted_path)
    # print(type(mounted_path))
    if mount_path + "/" not in mounted_path:
        response = enable_transit_secrets_engine(
            client=client,
            path=mount_path,
        )
        # print(response)
        # print(type(response))

    # print("create_key")
    response = client.secrets.transit.create_key(name="demo-key")
    # print(response)
    # print("read_key")
    response = client.secrets.transit.read_key(name="demo-key")
    # pprint.pprint(response)

    ############
    # userpass #
    ############
    # enable secrets engine
    mount_path = "userpass"
    mounted_path = client.sys.list_auth_methods()
    # pprint.pprint(mounted_path)
    # print(type(mounted_path))
    if mount_path + "/" not in mounted_path:
        response = enable_userpass_auth_method(
            client=client,
            path=mount_path,
        )
        # print(response)
        # print(type(response))

    print("create_or_update_user")
    response = client.auth.userpass.create_or_update_user(
        username="tsukuda",
        password="password",
        policies=["transit-writer", "admin"]
    )
    # print(response)

    ########
    # totp #
    ########
    mounted_path = client.sys.list_mounted_secrets_engines()
    mount_path = "totp"
    if mount_path + "/" not in mounted_path:
        response = enable_totp_secrets_engine(
            client=client,
            mount_point=mount_path,
        )

    # pprint.pprint(mounted_path)

    response = create_totp_key(
        client=client,
        name="tsukuda",
        mount_point="totp",
        account_name="tsukuda@picolab.jp"
    )
    # pprint.pprint(response)

    response = read_totp_code(client=client, name="tsukuda")
    pprint.pprint(response)
    # print(response["data"])
    send_email(
        subject="send your password",
        body=response["data"]["code"],
        sender="tsukudamayo@gmail.com",
        recipients=["tsukuda.m@picolab.jp"],
    )

    print("username: ", end="")
    username = input()
    print("password: ", end="")
    password = input()

    response = veriry_totp_code(
        client=client,
        name=username,
        code=password,
    )
    pprint.pprint(response)

    if response["data"]["valid"] is False:
        print("wrong password")
        sys.exit(1)
    else:
        print("OK")

    print("read_user")
    response = client.auth.userpass.read_user(username="tsukuda")
    # pprint.pprint(response)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--decrypt",
        "-d",
        help="decrypts the password of the user",
    )
    parser.add_argument(
        "--encrypt",
        "-e",
        help="encrypts the password of the user",
    )
    args = parser.parse_args()
    # print("args : ", args)

    if args.encrypt:
        print("Password: ", end="")
        password = input()
        print(password)
        print("login")
        response = client.auth.userpass.login(
            username=args.encrypt,
            password=password,
        )
        # print(response)

        ciphertext = transit_encrypt(
            client=client,
            plain_text=password,
            encrypt_key="demo-key",
        )
        connection = psql_connection(
            client=client,
            role="admin",
        )

        psql_input(
            "insert into users (username, password) values (%s, %s);",
            username=args.encrypt,
            ciphertext=ciphertext,
            connection=connection,
        )
        print("Successfully created new account for {}".format(args.encrypt))
    elif args.decrypt:
        connection = psql_connection(
            client=client,
            role="readonly",
        )
        ciphertext = psql_retrieval(
            sql_statement="select password from users where username=%s;",
            username=args.decrypt,
            connection=connection,
        )
        print("cipertext : ", ciphertext[-1][0])
        plaintext = transit_decrypt(
            client=client,
            ciphertext=ciphertext[-1][0],
            decrypt_key="demo-key",
            )

        print("The password for {} is {}.".format(args.decrypt, plaintext))


if __name__ == "__main__":
    main()
