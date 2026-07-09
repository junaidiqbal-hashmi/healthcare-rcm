from pathlib import Path
import yaml

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Config folder
CONFIG_DIR = PROJECT_ROOT / "config"


def load_yaml(filename: str) -> dict:
    """Load a YAML configuration file."""
    filepath = CONFIG_DIR / filename

    with open(filepath, "r") as file:
        return yaml.safe_load(file)


def get_files_config():
    return load_yaml("files.yaml")


def get_paths_config():
    return load_yaml("paths.yaml")


def get_database_config():
    return load_yaml("database.yaml")


def get_logging_config():
    return load_yaml("logging.yaml")