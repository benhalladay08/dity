"""
Commands for creating and managing the active project.

Commands:
- `dity proj create <name>`: Create a new project with the given name.
- `dity proj list`: List all existing projects.
- `dity proj activate <name>`: Set the specified project as the active project.
- `dity proj deactivate`: Deactivate the current active project.
- `dity proj delete <name>`: Delete the specified project.
- `dity proj info`: Display information about the active project.
"""

import argparse
import sys
from dity.project.manager import ProjectManager


# Create a shared ProjectManager instance
_project_manager = ProjectManager()


def setup_parser(subparsers) -> argparse.ArgumentParser:
    """Set up the proj command parser.
    
    Args:
        subparsers: The subparsers object from the main parser
        
    Returns:
        The proj parser
    """

    proj_parser = subparsers.add_parser(
        "proj",
        help="Manage dity projects"
    )
    
    proj_subparsers = proj_parser.add_subparsers(dest="proj_command", help="Project commands")
    
    # ----- proj create command -----
    create_parser = proj_subparsers.add_parser(
        "create",
        help="Create a new project"
    )
    create_parser.add_argument(
        "name",
        help="Name of the project to create"
    )

    # ----- proj list command -----
    list_parser = proj_subparsers.add_parser(
        "list",
        help="List all existing projects"
    )

    # ----- proj activate command -----
    activate_parser = proj_subparsers.add_parser(
        "activate",
        help="Activate a project"
    )
    activate_parser.add_argument(
        "name",
        help="Name of the project to activate"
    )
    # ----- proj deactivate command -----
    deactivate_parser = proj_subparsers.add_parser(
        "deactivate",
        help="Deactivate the current active project"
    )

    # ----- proj delete command -----
    delete_parser = proj_subparsers.add_parser(
        "delete",
        help="Delete a project"
    )
    delete_parser.add_argument(
        "name",
        help="Name of the project to delete"
    )

    # ----- proj info command -----
    info_parser = proj_subparsers.add_parser(
        "info",
        help="Display information about the active project"
    )

    return proj_parser


def handle_command(args) -> int:
    """Handle proj commands.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if args.proj_command == "create":
        return handle_create(args)
    elif args.proj_command == "list":
        return handle_list(args)
    elif args.proj_command == "activate":
        return handle_activate(args)
    elif args.proj_command == "deactivate":
        return handle_deactivate(args)
    elif args.proj_command == "delete":
        return handle_delete(args)
    elif args.proj_command == "info":
        return handle_info(args)
    else:
        print("✗ Error: No project command specified", file=sys.stderr)
        print("Use 'dity proj -h' for help", file=sys.stderr)
        return 1
    

def handle_create(args) -> int:
    """Handle the proj create command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        project_file = _project_manager.create_project(args.name)
        print(f"✓ Created project '{args.name}'")
        print(f"  Location: {project_file}")
        return 0
    except FileExistsError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1
    
def handle_list(args) -> int:
    """Handle the proj list command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        projects = _project_manager.list_projects()
        if not projects:
            print("No projects found.")
        else:
            print("Existing projects:")
            for proj in projects:
                print(f"- {proj}")
        return 0
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1
    
def handle_activate(args) -> int:
    """Handle the proj activate command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        _project_manager.activate_project(args.name)
        print(f"✓ Activated project '{args.name}'")
        return 0
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1
    
def handle_deactivate(args) -> int:
    """Handle the proj deactivate command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        _project_manager.deactivate_project()
        print("✓ Deactivated active project")
        return 0
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1
    
def handle_delete(args) -> int:
    """Handle the proj delete command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """

    # --- First, confirm deletion ---
    print(f"⚠️  You are about to delete the project '{args.name}'. This action cannot be undone.")
    confirm = input("Are you sure you want to delete this project? Type project name to confirm:\n")
    if confirm.lower() != args.name.lower():
        print("✗ Deletion cancelled.")
        return 1
    
    # --- Run deletion ---
    try:
        _project_manager.delete_project(args.name)
        print(f"✓ Deleted project '{args.name}'")
        return 0
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1
    
def handle_info(args) -> int:
    """Handle the proj info command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        active_project_name = _project_manager.get_active_project()
        if not active_project_name:
            print("No active project.")
            return 0
        
        project = _project_manager.get_project(active_project_name)
        if not project:
            print(f"✗ Error: Active project '{active_project_name}' not found", file=sys.stderr)
            return 1

        # TODO: Separate this into it's own formatter class later
        print(f"Active Project: {project.name}")
        print(f"Path: {project.path}")
        if project.routing:
            print(f"Routing: {project.routing}")
        else:
            print("Routing: None")
        
        return 0
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1