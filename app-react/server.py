"""Compatibility launcher for the modular Golden Monkey FastAPI backend."""

from backend.app import app
from backend.cli import main

__all__ = ["app", "main"]


if __name__ == "__main__":
    main()
