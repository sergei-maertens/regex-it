import json
from base64 import b64encode

from django.conf import settings
from django.utils.crypto import get_random_string

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from requests import Session

from .utils import build_url


def create_access_token(session: Session, expiration: str = "30 minutes") -> str:
    private_key = serialization.load_pem_private_key(
        settings.TRANSIP_PRIVATE_KEY,
        password=None,
    )
    nonce = get_random_string(length=16)
    data = {
        "login": settings.TRANSIP_AUTH_USERNAME,
        "nonce": nonce,
        "read_only": True,
        "expiration_time": expiration,
        "label": f"website-expenses-integration-{get_random_string()}",
        "global_key": True,
    }

    serialized = json.dumps(data, allow_nan=False).encode("utf-8")

    signature = private_key.sign(serialized, padding.PKCS1v15(), hashes.SHA512())
    encoded_signature = b64encode(signature).decode("ascii")
    response = session.post(
        build_url("auth"),
        data=serialized,
        headers={
            "Content-Type": "application/json",
            "Signature": encoded_signature,
        },
    )
    response.raise_for_status()

    token = response.json()["token"]
    session.headers["Authorization"] = f"Bearer {token}"
    return token
