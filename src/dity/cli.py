"""CLI interface for dity."""
import argparse
from dity import __version__


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
    
    args = parser.parse_args()


if __name__ == "__main__":
    main()
