from dity.project.classes.routing import Routing
from dity.project.mapping.base import BaseMapper

class RoutingMapper(BaseMapper[Routing]):
    """Class responsible for mapping routing data to Routing objects."""
    
    def to_dict(self, obj: Routing) -> dict:
        """Convert a Routing object to a dictionary representation."""
        return {
            "sources": obj.sources,
            "destinations": obj.destinations,
        }
    
    def from_dict(self, data: dict) -> Routing:
        """Create a Routing object from a dictionary representation."""
        return Routing(
            sources=data["sources"],
            destinations=data["destinations"],
        )