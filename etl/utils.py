import yaml
import logging
from typing import Any
from pathlib import Path
from pydantic import ValidationError
from config_schema import ETLConfig

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> dict[str, Any]:
    """
    load and validates pipeline configuration from a yaml file.

    Args:
        config_path (str): path to the yaml config file.

    Returns:
        dict: config dict.
    """
    config_path = Path(config_path)
    if not config_path.exists():
        logger.error(f"config file not found at: {config_path}")
        raise FileNotFoundError(f"config file not found at {config_path}")

    try:
        with open(config_path, "r") as f:
            raw_config = yaml.safe_load(f)
        logger.info("config file loaded")
    except yaml.YAMLError as e:
        logger.error(f"failed to parse yaml config file: {e}")
        raise ValueError(f"invalid yml syntax in config file:\n{e}")

    try:
        validated_config = ETLConfig(**raw_config)
        logger.info("config file validated.")
        return validated_config.dict()
    except ValidationError as e:
        logger.error(f"invalid configuration file structure:\n{e}")
        raise ValueError(f"invalid configuration file:\n{e}")
