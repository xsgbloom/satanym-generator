"""Satanym: A deterministic name registry and generator service.

Copyright 2026 Frogg XSG
(License omitted for brevity)
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from config import SatanymConfig
from storage import StorageProvider


class SatanymRegistry:
    """Business logic for identity registration and suggestions."""

    def __init__(self, config: SatanymConfig, storage_provider: StorageProvider):
        """Initializes registry with config and storage.

        Args:
            config: An instance of SatanymConfig.
            storage_provider: An instance of StorageProvider.
        """
        self.config = config
        self.storage = storage_provider

    def load_names(self, filename: str) -> List[str]:
        """Loads a list of names, defaulting to ['Sovereign']."""
        content = self.storage.read_text(filename)
        lines = content.splitlines()
        names = [line.strip() for line in lines if line.strip()]
        return names if names else ["Sovereign"]

    def add_to_pool(self, filename: str, name: str):
        """Adds a unique name to the list pool."""
        current_names = self.load_names(filename)
        if name.lower() not in [item.lower() for item in current_names]:
            current_names.append(name)
            self.storage.write_text(filename, "\n".join(current_names))

    def get_registry_data(self) -> Tuple[Dict[str, str], Optional[int]]:
        """Fetches identity mapping and current version ID."""
        path = self.config.registry_file
        exists, generation_id = self.storage.get_metadata(path)
        if exists:
            data = self.storage.read_text(path)
            return json.loads(data), generation_id
        return {}, None

    def register_user(
        self,
        hash_value: str,
        first_name: str,
        last_name: Optional[str]
    ) -> Dict:
        """Attempts to register a new identity."""
        registry, generation_id = self.get_registry_data()
        clean_first = first_name.strip()
        clean_last = (last_name or "").strip()
        full_name = f"{clean_first} {clean_last}".strip()

        if full_name.lower() in [val.lower() for val in registry.values()]:
            return {"error": "Identity claimed"}

        registry[hash_value] = full_name
        try:
            self.storage.write_text(
                self.config.registry_file, json.dumps(registry), generation_id
            )
        except Exception:
            return {"error": "Conflict"}

        self.add_to_pool(self.config.first_name_file, clean_first)
        if last_name:
            self.add_to_pool(self.config.last_name_file, clean_last)

        return {"success": True, "full_name": full_name}

    def suggest_name(self, hash_value: str) -> str:
        """Generates a deterministic name suggestion."""
        registry, _ = self.get_registry_data()
        first_names = self.load_names(self.config.first_name_file)
        last_names = self.load_names(self.config.last_name_file)
        existing_lower = [val.lower() for val in registry.values()]

        for attempt in range(101):
            random.seed(f"{hash_value}{attempt}")
            idx_f = random.randint(0, self.config.seed_limit - 1) % len(
                first_names
            )
            idx_l = random.randint(0, self.config.seed_limit - 1) % len(
                last_names
            )
            f_cand = first_names[idx_f]
            l_cand = last_names[idx_l]

            if f_cand.lower() == l_cand.lower() and len(first_names) > 1:
                continue

            full_candidate = f"{f_cand} {l_cand}"
            if full_candidate.lower() not in existing_lower:
                return full_candidate

        return "Nameless Rebel"
