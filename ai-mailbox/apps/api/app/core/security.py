from datetime import datetime, timedelta
from typing import Optional
import hmac
import hashlib
import base64

from .config import settings


def sign_payload(payload: str, expires_in_seconds: int = 300) -> str:
    expires = int((datetime.utcnow() + timedelta(seconds=expires_in_seconds)).timestamp())
    msg = f"{payload}.{expires}".encode()
    sig = hmac.new(settings.api_secret.encode(), msg, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(msg + b"." + sig).decode()
    return token


def verify_signature(token: str) -> Optional[str]:
    try:
        raw = base64.urlsafe_b64decode(token.encode())
        parts = raw.split(b".")
        if len(parts) != 3:
            return None
        payload, exp, sig = parts[0], parts[1], parts[2]
        msg = payload + b"." + exp
        expected = hmac.new(settings.api_secret.encode(), msg, hashlib.sha256).digest()
        if not hmac.compare_digest(sig, expected):
            return None
        if int(exp.decode()) < int(datetime.utcnow().timestamp()):
            return None
        return payload.decode()
    except Exception:
        return None
