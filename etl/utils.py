import yaml
from typing import Any

def load_config(config_path: str = "config/config.yaml") -> dict[str, Any]:
    """
    load pipeline configuration from a YAML file.

    Args:
        config_path (str): path to the yaml config file.

    Returns:
        dict: config dict.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
