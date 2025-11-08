from pathlib import Path
from typing import Any

from dity.project.classes.project import Project
from dity.project.mapping.base import BaseMapper
from dity.project.mapping.routing import RoutingMapper

class ProjectMapper(BaseMapper[Project]):
    """Class responsible for mapping project data to Project objects."""
    def __init__(self, routing_mapper: BaseMapper | None = None) -> None:
        self.routing_mapper = routing_mapper or RoutingMapper()

    def to_dict(self, obj: Project) -> dict:
        """Convert a Project object to a dictionary representation."""

        data: dict[str, Any] = {
            "name": obj.name,
            "path": str(obj.path),
        }

        # --- Optional fields ---
        if obj.routing:
            data["routing"] = self.routing_mapper.to_dict(obj.routing)

        return data
    
    def from_dict(self, data: dict) -> Project:
        """Create a Project object from a dictionary representation."""

        routing = None
        if "routing" in data and data["routing"] is not None:
            routing = self.routing_mapper.from_dict(data["routing"])

        project = Project(
            name=data["name"],
            path=Path(data["path"]),
            routing=routing
        )

        return project