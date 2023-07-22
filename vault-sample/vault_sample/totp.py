from hvac import utils
import hvac
import requests
from typing import Any, Dict


DEFAULT_MOUNT_POINT = "totp"


def enable_totp_secrets_engine(
    client: hvac.Client,
    mount_point: str = DEFAULT_MOUNT_POINT,
) -> requests.models.Response:
    return client.sys.enable_secrets_engine(
        backend_type="totp",
        path=mount_point,
    )

def create_totp_key(
    client: hvac.Client,
    name: str,
    account_name: str,
    mount_point: str = DEFAULT_MOUNT_POINT,
) -> requests.models.Response:
    return client.write(
        path=f"/{mount_point}/keys/{name}",
        generate=True,
        key_size=20,
        issuer="Vault",
        account_name=account_name,
        mount_point="totp",
        period=30,
    )


def read_totp_code(
    client: hvac.Client,
    name: str,
) -> Any:
    return client.read("/totp/code/" + name)


def veriry_totp_code(
    client: hvac.Client,
    name: str,
    code: str,
) -> Dict:
    return client.write(
        f"/totp/code/{name}",
        code=code,
    )
    
