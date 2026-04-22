"""Satanym: A deterministic name registry and generator service.

Copyright 2026 Frogg XSG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import hashlib
import json

import uvicorn
from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from config import SatanymConfig
from registry import SatanymRegistry
from storage import StorageProvider

app = FastAPI()

APP_CONFIG = SatanymConfig()
_STORAGE_PROVIDER = StorageProvider(APP_CONFIG)
_REGISTRY_LOGIC = SatanymRegistry(APP_CONFIG, _STORAGE_PROVIDER)


def get_registry() -> SatanymRegistry:
    """Dependency provider for the SatanymRegistry logic."""
    return _REGISTRY_LOGIC


@app.middleware("http")
async def sentry_gate(request: Request, call_next):
    """Cloud Run stealth gate for zero-cost obfuscation."""
    header_host = request.headers.get("host", "").lower().split(":")[0]

    if (header_host not in APP_CONFIG.allowed_hosts or
            request.url.path != APP_CONFIG.ritual_path):
        await request.scope["send"]({"type": "http.disconnect"})
        return Response(status_code=None)

    return await call_next(request)


@app.post(APP_CONFIG.ritual_path)
async def handle_post(
    request: Request,
    registry: SatanymRegistry = Depends(get_registry)
):
    """Processes secret hashing and registration status."""
    try:
        request_data = await request.json()
        secret_value = request_data.get("secret", "").strip().lower()
        if not secret_value:
            return {"error": "Secret required"}

        hash_value = hashlib.sha256(secret_value.encode()).hexdigest()
        registry_data, _ = registry.get_registry_data()

        response_payload = {
            "hash": hash_value,
            "registered": hash_value in registry_data
        }
        if response_payload["registered"]:
            response_payload["full_name"] = registry_data[hash_value]
        return response_payload
    except (json.JSONDecodeError, KeyError):
        return Response(status_code=400)


@app.get(APP_CONFIG.ritual_path)
async def handle_get(
    hash_value: str = None,
    register_flag: int = 0,
    first_name: str = None,
    last_name: str = None,
    registry: SatanymRegistry = Depends(get_registry)
):
    """UI delivery, Name Suggestion, or Registration."""
    if not hash_value:
        # Note: In a true DI pattern, StorageProvider would also be injected
        index_html = _STORAGE_PROVIDER.read_text("index.html")
        return HTMLResponse(content=index_html or "Error")

    hash_value = hash_value.strip().lower()
    registry_data, _ = registry.get_registry_data()

    if hash_value in registry_data:
        return {"full_name": registry_data[hash_value]}

    if register_flag == 1 and first_name:
        return registry.register_user(hash_value, first_name, last_name)

    return {"full_name": registry.suggest_name(hash_value)}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=APP_CONFIG.server_port,
        workers=1
    )
