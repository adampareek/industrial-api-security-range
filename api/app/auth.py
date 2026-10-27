import base64
import json
import os
import time
from typing import Any

import jwt
from fastapi import HTTPException, Request

from .state import PROFILES

def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)

def _unsafe_decode_none(token: str) -> dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("malformed JWT")
    header = json.loads(_b64url_decode(parts[0]))
    payload = json.loads(_b64url_decode(parts[1]))
    if header.get("alg") != "none":
        raise ValueError("not an unsigned token")
    return payload

def issue_token(profile_id: int) -> str:
    profile = PROFILES[profile_id]
    secret = os.getenv("LAB_JWT_SECRET", "731942")
    payload = {
        "sub": profile["username"],
        "profile_id": profile["id"],
        "role": profile["role"],
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "iss": "industrial-api-security-range",
        "aud": "range-api",
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def validate_token(token: str) -> dict[str, Any]:
    mode = os.getenv("LAB_MODE", "vulnerable").lower()
    if mode == "vulnerable":
        try:
            header = jwt.get_unverified_header(token)
        except jwt.PyJWTError as exc:
            raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc
        if header.get("alg") == "none":
            try:
                return _unsafe_decode_none(token)
            except Exception as exc:
                raise HTTPException(status_code=401, detail="Invalid unsigned token") from exc
    secret = os.getenv("LAB_JWT_SECRET", "731942")
    try:
        return jwt.decode(token, secret, algorithms=["HS256"], audience="range-api", issuer="industrial-api-security-range")
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc

def token_from_request(request: Request) -> dict[str, Any]:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    return validate_token(auth.removeprefix("Bearer ").strip())
