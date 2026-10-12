"""Logging configuration shared by the command-line entry points."""

import logging


def setup_logging() -> None:
    """Send messages of level INFO and above to the terminal, with the time."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
