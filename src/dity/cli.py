"""CLI interface for dity."""
import argparse
import sys
from dity import __version__
from dity.commands import proj


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="dity",
        description="A DIT tool to DIY - Python CLI tool for DITs on set and editors in post",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"dity {__version__}",
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Register proj command
    proj.setup_parser(subparsers)
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "proj":
        exit_code = proj.handle_command(args)
        sys.exit(exit_code)
    elif args.command is None:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
