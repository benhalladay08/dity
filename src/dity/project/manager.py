"""Project management functionality."""
import datetime
import json
import platform
from pathlib import Path
from typing import Optional

from dity.project.classes.project import Project
from dity.project.mapping.project import ProjectMapper


class ProjectManager:
    """Class responsible for managing DIT projects."""
    def __init__(self, mapper: ProjectMapper | None = None) -> None:
        self.mapper = mapper or ProjectMapper()
        
        # --- get projects directory ---
        home = Path.home()
        self.projects_dir = home / ".dity" / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    # ===========================================================
    # Project Creation
    # ===========================================================

    def create_project(self, name: str) -> Path:
        """Create a new project with the given name.
        
        Args:
            name: The name of the project to create
            
        Returns:
            Path to the created project config.json file
            
        Raises:
            FileExistsError: If a project with the same name already exists
            ValueError: If the project name is invalid
        """

        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")

        name = name.strip()

        # Create project directory
        project_dir = self.projects_dir / name
        
        if project_dir.exists():
            raise FileExistsError(f"Project '{name}' already exists")
        
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Config file inside project directory
        project_file = project_dir / "config.json"
        
        # --- Create project data using the mapper ---
        project = Project(name=name, path=project_file, routing=None)

        project = self.pre_create_project(project)

        # --- Map to dict ---
        project_data = self.mapper.to_dict(project)

        # --- Write project file ---
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2)
        
        return project_file
    
    def pre_create_project(self, proj: Project) -> Project:
        """Hook method called before creating a project.
        
        Args:
            proj: The Project object about to be created

        Returns:
            The same Project object
        """
        return proj
    
    # ===========================================================
    # Project Retrieval
    # ===========================================================

    def project_exists(self, name: str) -> bool:
        """Check if a project with the given name exists.
        
        Args:
            name: The name of the project to check
            
        Returns:
            True if the project exists, False otherwise
        """
        project_dir = self.projects_dir / name.strip()
        return project_dir.exists() and (project_dir / "config.json").exists()
    
    def get_project(self, name: str) -> Optional[Project]:
        """Get project data by name.
        
        Args:
            name: The name of the project to retrieve
            
        Returns:
            Project object, or None if project doesn't exist
        """
        project_dir = self.projects_dir / name.strip()
        project_file = project_dir / "config.json"
        
        if not project_file.exists():
            return None
        
        with open(project_file, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        return self.mapper.from_dict(project_data)
    
    def list_projects(self) -> list[str]:
        """List all existing project names.
        
        Returns:
            List of project names
        """
        # Get all directories that contain a config.json
        project_names = []
        for item in self.projects_dir.iterdir():
            if item.is_dir() and (item / "config.json").exists():
                project_names.append(item.name)
        return project_names
    
    # ===========================================================
    # Project Activation
    # ===========================================================

    def activate_project(self, name: str) -> None:
        """Activate a project by name.
        
        Args:
            name: The name of the project to activate
            
        Raises:
            FileNotFoundError: If the project does not exist
        """

        if not self.project_exists(name):
            raise FileNotFoundError(f"Project '{name}' does not exist")
        
        # Write active project to a file
        active_file = self.projects_dir / "active_project.json"
        data = {
            "active_project": name,
            "time_activated": datetime.datetime.now().isoformat()
        }

        with open(active_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def deactivate_project(self) -> None:
        """Deactivate the currently active project."""
        active_file = self.projects_dir / "active_project.json"
        
        if active_file.exists():
            active_file.unlink()

    def get_active_project(self) -> Optional[str]:
        """Get the name of the currently active project.
        
        Returns:
            The name of the active project, or None if no project is active
        """
        active_file = self.projects_dir / "active_project.json"
        
        if not active_file.exists():
            return None
        
        with open(active_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get("active_project", None)

    # ===========================================================
    # Project Deletion
    # ===========================================================

    def delete_project(self, name: str) -> None:
        """Delete a project by name.
        
        Args:
            name: The name of the project to delete
            
        Raises:
            FileNotFoundError: If the project does not exist
        """
        project_dir = self.projects_dir / name.strip()
        
        if not project_dir.exists():
            raise FileNotFoundError(f"Project '{name}' does not exist")
        
        # Remove all files in the project directory
        for file in project_dir.iterdir():
            if file.is_file():
                file.unlink()
        
        # Remove the directory itself
        project_dir.rmdir()