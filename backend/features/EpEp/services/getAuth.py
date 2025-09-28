import hmac
import hashlib
import datetime
import os
import requests
import hmac
import hashlib
from datetime import datetime
import json

from models.auth import Auth
from config.paths import EpEpPaths


def get_auth_token():
    app_token = os.getenv("EPP_TEST_APP_TOKEN")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {app_token}",
    }
    body = generate_hash()
    response = requests.post(EpEpPaths.GetToken, headers=headers, data=body)
    response.raise_for_status()
    auth_response = response.json()

    Auth(auth_response["token"], auth_response["expiresIn"])


def generate_hash():
    app_secret = os.getenv("EPEP_TEST_APP_SECRET")
    if app_secret is None:
        raise ValueError("EPEP_TEST_APP_SECRET environment variable not set")

    app_secret_bytes = app_secret.encode("utf-8")
    now = datetime.now()
    data = now.strftime("%Y%m%d%H%M%S") + f"{int(now.microsecond/1000):03d}"
    digest = hmac.new(
        app_secret_bytes, data.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return json.dumps({"data": data, "hash": digest}, ensure_ascii=False, indent=2)
