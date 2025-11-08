from dataclasses import dataclass

@dataclass
class Routing:
    """Class representing routing information for a DIT project."""
    
    sources: list
    destinations: list