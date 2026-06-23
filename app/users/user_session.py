from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time


SESSION_SECRET = os.getenv("SESSION_SECRET", "change-me-in-production")
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", str(60 * 60 * 24 * 7)))


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64decode(raw: str) -> bytes:
    padding = "=" * (-len(raw) % 4)
    return base64.urlsafe_b64decode(f"{raw}{padding}")


def create_session_token(*, user_id: int, username: str) -> str:
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": int(time.time()) + SESSION_TTL_SECONDS,
    }
    payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_part = _b64encode(payload_bytes)
    signature = hmac.new(
        SESSION_SECRET.encode("utf-8"),
        payload_part.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return f"{payload_part}.{_b64encode(signature)}"


def decode_session_token(token: str) -> dict[str, int | str]:
    try:
        payload_part, signature_part = token.split(".", 1)
    except ValueError as exc:
        raise ValueError("Invalid session token.") from exc

    expected_signature = hmac.new(
        SESSION_SECRET.encode("utf-8"),
        payload_part.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    actual_signature = _b64decode(signature_part)

    if not hmac.compare_digest(expected_signature, actual_signature):
        raise ValueError("Invalid session token.")

    payload = json.loads(_b64decode(payload_part).decode("utf-8"))
    if int(payload["exp"]) < int(time.time()):
        raise ValueError("Session has expired.")

    return payload
