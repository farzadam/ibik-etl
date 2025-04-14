import argparse
from logging_config import setup_logging
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from etl.utils import load_config
import logging

setup_logging() 
logger = logging.getLogger(__name__)

def main(config_path: str = "config/config.yaml") -> None:
    """
    main ETL pipeline runner.
    it loads configuration and runs extract, transform, and load steps.
    """
    config = load_config(config_path)
    df = extract_data(config["data"])
    df_clean = transform_data(df, config["transform"])
    load_data(df_clean, config["load"])
    logger.info("ETL pipeline completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ETL pipeline")
    parser.add_argument(
        "--config", 
        type=str, 
        default="config/config.yaml", 
        help="Path to the YAML config file"
    )
    args = parser.parse_args()
    main(args.config)