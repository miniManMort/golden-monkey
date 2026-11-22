"""Command-line entry point for the FastAPI application."""

import argparse

import uvicorn

from .app import app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Golden Monkey React web app.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)
