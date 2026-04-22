"""Satanym: A deterministic name registry and generator service.

Copyright 2026 Frogg XSG
(License omitted for brevity, but same as config.py)
"""

import os
from typing import Optional, Tuple
from google.cloud import storage
from config import SatanymConfig


class StorageProvider:
    """A reusable handler for managing GCS and local file storage.

    Example:
        config_instance = SatanymConfig()
        storage_provider = StorageProvider(config_instance)
    """

    def __init__(self, config: SatanymConfig):
        """Initializes storage based on provided configuration.

        Args:
            config: An instance of SatanymConfig.
        """
        self.config = config
        self.storage_client = storage.Client() if config.bucket_name else None

    def _get_blob(self, filename: str):
        """Internal helper to retrieve a GCS blob.

        Args:
            filename: Name of the file in the bucket.

        Returns:
            storage.Blob: The GCS blob object or None.
        """
        if self.storage_client and self.config.bucket_name:
            bucket = self.storage_client.bucket(self.config.bucket_name)
            return bucket.blob(filename)
        return None

    def read_text(self, filename: str) -> str:
        """Reads text content from GCS or local disk.

        Args:
            filename: Path to the file or name of the blob.

        Returns:
            str: The file contents or an empty string if missing.
        """
        blob = self._get_blob(filename)
        if blob and blob.exists():
            return blob.download_as_text()

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file_handle:
                return file_handle.read()
        return ""

    def write_text(
        self,
        filename: str,
        content: str,
        generation_id: Optional[int] = None
    ):
        """Writes text to storage with GCS concurrency support.

        Args:
            filename: Target file/blob name.
            content: Text data to write.
            generation_id: Generation ID for GCS concurrency control.
        """
        blob = self._get_blob(filename)
        if blob:
            blob.upload_from_string(
                content, if_generation_match=generation_id
            )
        else:
            with open(filename, "w", encoding="utf-8") as file_handle:
                file_handle.write(content)

    def get_metadata(self, filename: str) -> Tuple[bool, Optional[int]]:
        """Returns existence and the generation ID for GCS files.

        Args:
            filename: The file to check.

        Returns:
            Tuple[bool, Optional[int]]: (file_exists, generation_id).
        """
        blob = self._get_blob(filename)
        if blob and blob.exists():
            blob.reload()
            return True, blob.generation
        return os.path.exists(filename), None
