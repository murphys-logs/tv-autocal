"""Running without options prints a simulation; importing does nothing."""

from .cli import entrypoint


if __name__ == "__main__":
    entrypoint()
