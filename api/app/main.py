import os
import uuid
from copy import deepcopy

import httpx
from fastapi import FastAPI, HTTPException, Request

from .auth import issue_token, token_from_request
from .models import BookmarkCreate, LoginRequest, PasswordReset
from .security import validate_external_url
from .state import ASSETS, BOOKMARKS, PROFILES

app = FastAPI(title="Industrial API Security Range", version="1.0.0", description="Synthetic intentionally vulnerable API for local security training.")

def mode() -> str:
    return os.getenv("LAB_MODE", "vulnerable").lower()

def public_profile(profile: dict) -> dict:
    item = deepcopy(profile)
    item.pop("password", None)
    return item

@app.get("/")
def root():
    return {"project": "Industrial API Security Range", "mode": mode(), "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "mode": mode()}

@app.post("/api/auth/token")
def login(data: LoginRequest):
    for profile_id, profile in PROFILES.items():
        if profile["username"] == data.username and profile["password"] == data.password:
            return {"access_token": issue_token(profile_id), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/assets")
def assets():
    if mode() == "vulnerable":
        return ASSETS
    safe_assets = deepcopy(ASSETS)
    for asset in safe_assets:
        asset["maintenance_note"] = "[redacted operational note]"
    return safe_assets

@app.get("/api/profiles/{profile_id}")
def get_profile(profile_id: int, request: Request):
    profile = PROFILES.get(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if mode() == "hardened":
        claims = token_from_request(request)
        if claims.get("profile_id") != profile_id and claims.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Object access denied")
    return public_profile(profile)

@app.post("/api/profiles/{profile_id}/reset-password")
def reset_password(profile_id: int, data: PasswordReset, request: Request):
    profile = PROFILES.get(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    claims = token_from_request(request)
    if mode() == "hardened":
        if claims.get("profile_id") != profile_id and claims.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Password reset denied")
    profile["password"] = data.new_password
    return {"status": "password-updated", "profile_id": profile_id}

@app.get("/api/admin/diagnostics")
def diagnostics(request: Request):
    claims = token_from_request(request)
    if claims.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return {"status": "diagnostics-enabled", "message": "Synthetic privileged endpoint reached.", "mode": mode()}

@app.post("/api/bookmarks", status_code=201)
def create_bookmark(data: BookmarkCreate):
    if mode() == "hardened":
        allowed, reason = validate_external_url(data.url)
        if not allowed:
            raise HTTPException(status_code=400, detail=reason)
    bookmark_id = str(uuid.uuid4())
    BOOKMARKS[bookmark_id] = {"id": bookmark_id, "url": data.url}
    return BOOKMARKS[bookmark_id]

@app.get("/api/bookmarks/{bookmark_id}")
async def get_bookmark(bookmark_id: str):
    bookmark = BOOKMARKS.get(bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    if mode() == "hardened":
        allowed, reason = validate_external_url(bookmark["url"])
        if not allowed:
            raise HTTPException(status_code=400, detail=reason)
    try:
        async with httpx.AsyncClient(follow_redirects=False, timeout=3.0) as client:
            response = await client.get(bookmark["url"])
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Preview fetch failed: {exc}") from exc
    return {**bookmark, "preview": response.text[:1000], "status_code": response.status_code}
