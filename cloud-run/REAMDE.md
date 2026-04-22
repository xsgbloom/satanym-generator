# Satanym Service

A deterministic, stealth-oriented name registry.

## Configuration
The following environment variables are required for deployment:
* `BUCKET_NAME`: GCS bucket for persistent storage.
* `ALLOWED_HOSTS`: Comma-separated list of valid Host headers.
* `RITUAL_PATH`: The secret endpoint path (e.g., `/satanym`).

## Security
This service utilizes ASGI-level connection resets to "black-hole" 
unauthorized requests, providing zero-cost obfuscation.
