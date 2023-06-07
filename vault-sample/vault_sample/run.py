import os
import pprint
import hvac


def main():
    client = hvac.Client(url="http://localhost:8200")
    print(client.is_authenticated())

    client.kv.default_kv_version = 2

    havc_secret = {
        "psst": "this is secret",
    }

    client.secrets.kv.v2.create_or_update_secret(
        path="hvac",
        secret=havc_secret,
    )

    print("Secret written successfully.")

    read_response = client.secrets.kv.read_secret_version(path="hvac")
    pprint.pprint(read_response)

    client.auth.github.configure(
        organization=os.getenv("GITHUB_ORG"),
        max_ttl='48h',  # i.e., A given token can only be renewed for up to 48 hours
    )
    
    github_auth_path = "github"
    description = "Auth method for use by team members in our company's Github organization"

    if '%s/' % github_auth_path not in client.sys.list_auth_methods()['data']:
        print('Enabling the github auth backend at mount_point: {path}'.format(
            path=github_auth_path,
        ))
        client.sys.enable_auth_method(
            method_type='github',
            description=description,
            path=github_auth_path,
        )

    login_response = client.auth.github.login(token=os.getenv("GITHUB_TOKEN"))
    pprint.pprint(login_response)

    read_response = client.secrets.kv.read_secret_version(path="hvac")
    pprint.pprint(read_response)
    
    delete_clients = client.secrets.kv.delete_metadata_and_all_versions("hvac")
    print(delete_clients)


if __name__ == "__main__":
    main()
