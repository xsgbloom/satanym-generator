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

import os


class SatanymConfig:
    """Encapsulates all environment configuration for the service.

    Example:
        configuration = SatanymConfig()
        print(configuration.bucket_name)
    """

    def __init__(self):
        """Initializes configuration from environment variables."""
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.registry_file = os.getenv("REGISTRY_FILE", "registry.json")
        self.first_name_file = os.getenv("FN_FILE", "first_names.txt")
        self.last_name_file = os.getenv("LN_FILE", "last_names.txt")
        self.seed_limit = int(os.getenv("SEED_LIMIT", "666"))
        self.ritual_path = os.getenv("RITUAL_PATH", "/satanym")
        self.server_port = int(os.getenv("PORT", "8000"))

        raw_hosts = os.getenv("ALLOWED_HOSTS", "satanym.miscreants.org")
        self.allowed_hosts = raw_hosts.lower().split(",")
