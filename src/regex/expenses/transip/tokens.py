import json
from base64 import b64decode, b64encode
from datetime import datetime

from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from requests import Request
from requests.auth import AuthBase

from .models import AccessToken
from .utils import build_url


def create_access_token(expiration: str = "30 minutes") -> str:
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
    response = requests.post(
        build_url("auth"),
        data=serialized,
        headers={
            "Content-Type": "application/json",
            "Signature": encoded_signature,
        },
    )
    response.raise_for_status()
    return response.json()["token"]


def get_access_token():
    token = (
        AccessToken.objects.filter(expires__gt=timezone.now())
        .order_by("expires")
        .first()
    )
    if token is not None:
        return token.token

    token = create_access_token()
    # just accept whatever is in the payload - I'm not sure we can even validate
    # the signature?
    payload = b64decode(token.split(".")[1].encode("ascii") + b"==")
    claims = json.loads(payload.decode("utf-8"))
    expiry = datetime.fromtimestamp(claims["exp"])
    AccessToken.objects.create(
        token=token,
        expires=timezone.make_aware(expiry),
    )
    return token


class TransipAuth(AuthBase):
    def __call__(self, request: Request):
        token = get_access_token()
        request.headers["Authorization"] = f"Bearer {token}"
        return request
