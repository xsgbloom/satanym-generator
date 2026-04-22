# Satanym Generator

**Satanym** is a deterministic name registry and generator service. It provides a FastAPI-based backend to suggest unique names based on secret hashes and maintains a permanent registry of claimed identities.

Built with a focus on "stealth" deployment, it includes features to prevent unwanted discovery on public cloud providers like Google Cloud Run.

## 🕸️ Features

- **Deterministic Generation**: Uses SHA-256 hashing to ensure a specific "secret" always maps to the same suggested name.
- **Persistent Registry**: Allows users to "claim" and register their generated names via a storage provider.
- **Stealth Gate Middleware**: Includes a custom middleware (`sentry_gate`) that drops connections if the `Host` header doesn't match your configuration, providing zero-cost obfuscation.
- **Dual Interface**: Supports both a JSON API for programmatic access and an HTML UI for manual "rituals."

## 🛠️ Architecture

- **FastAPI**: The core web framework.
- **Uvicorn**: ASGI server for high-performance delivery.
- **StorageProvider**: Abstraction layer for reading/writing registry data (supports local or cloud storage).
- **SatanymRegistry**: Core logic for name suggestion and registration validation.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- Dependencies: `fastapi`, `uvicorn`, `hashlib` (standard lib), and any custom logic in your `config.py`, `registry.py`, and `storage.py` files.

### 2. Configuration
The application relies on a `SatanymConfig` object. Ensure your `config.py` defines the following:
- `allowed_hosts`: A list of hostnames permitted to access the service.
- `ritual_path`: The specific URL path where the service lives (e.g., `/the-ritual`).
- `server_port`: The port for the Uvicorn server.

### 3. Installation
```bash
git clone [https://github.com/xsgbloom/satanym-generator.git](https://github.com/xsgbloom/satanym-generator.git)
cd satanym-generator
pip install -r requirements.txt
