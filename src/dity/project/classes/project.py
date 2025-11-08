"""
Project class for managing project metadata and files.

Attributes:
- name (str): The name of the project.
- path (str): The file system path to the project directory.
- routing (Routing | None): Optional routing information associated with the project.
"""

from dataclasses import dataclass
from pathlib import Path

from dity.project.classes.routing import Routing

@dataclass
class Project:
    """Class representing a DIT project."""
    
    name: str
    path: Path
    routing: Routing | None