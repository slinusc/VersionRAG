"""
Schema for documentation_register.json.

The register is the single source of truth for VersionRAG indexing.
To add new documentation: add an entry to documentation_register.json and run the indexer.
"""

from typing import Optional, List, Literal
from pydantic import BaseModel
from pathlib import Path
import json


class Version(BaseModel):
    """A specific version of documentation or changelog."""
    version: str
    file: str


class Collection(BaseModel):
    """A collection of versioned documentation or changelog files."""
    name: str
    category: str
    description: str
    type: Literal["documentation", "changelog"]
    versions: List[Version]


class Register(BaseModel):
    """
    Documentation register - single source of truth for indexing.

    Load from JSON:
        register = Register.load("path/to/documentation_register.json")

    Convert to FileAttributes for indexer:
        attributes = register.to_file_attributes(base_path="/path/to/data")
    """
    base_path: Optional[str] = None
    collections: List[Collection]

    class Config:
        extra = "ignore"  # Ignore unknown fields like _comment

    @classmethod
    def load(cls, filepath: str) -> 'Register':
        """Load register from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)

    def to_file_attributes(self, base_path: Optional[str] = None):
        """
        Convert register to FileAttributes list for the indexing pipeline.

        Args:
            base_path: Base path for resolving relative file paths.
        """
        from indexing.versionrag_indexer_extract_attributes import FileAttributes, FileType

        resolve_base = Path(base_path) if base_path else (Path(self.base_path) if self.base_path else None)

        attributes = []
        for collection in self.collections:
            file_type = FileType.Changelog if collection.type == "changelog" else FileType.WithoutChangelog

            for version in collection.versions:
                file_path = str(resolve_base / version.file) if resolve_base else version.file

                attributes.append(FileAttributes(
                    data_file=file_path,
                    type=file_type,
                    documentation=collection.name,
                    description=collection.description,
                    version=version.version,
                    additional_attributes={"category": collection.category}
                ))

        return attributes

    def stats(self) -> dict:
        """Get register statistics."""
        docs = [c for c in self.collections if c.type == "documentation"]
        changelogs = [c for c in self.collections if c.type == "changelog"]

        return {
            "collections": len(self.collections),
            "documentation": len(docs),
            "changelogs": len(changelogs),
            "total_versions": sum(len(c.versions) for c in self.collections),
        }
