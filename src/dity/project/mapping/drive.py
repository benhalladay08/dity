from pathlib import Path

from dity.project.classes.drives import Drive
from dity.project.mapping.base import BaseMapper

class DriveMapper(BaseMapper[Drive]):
    def to_dict(self, obj: Drive) -> dict:
        """Convert a Drive object to a dictionary"""
        return {
                "name": obj.name,
                "path": str(obj.path),
                "type": obj.type,
                "structure": obj.structure
                }

    def from_dict(self, data: dict) -> Drive:
        """Create a Drive object from a dictionary"""
        return Drive(
                name=data["name"],
                path=Path(data["path"]),
                type=data["type"],
                structure=data["structure"]
        )
