from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from etl.utils import load_config

def main() -> None:
    """
    main ETL pipeline runner.
    it loads configuration and runs extract, transform, and load steps.
    """
    config = load_config("config/config.yaml")
    df = extract_data(config["data"])
    df_clean = transform_data(df, config["transform"])
    load_data(df_clean, config["load"])

if __name__ == "__main__":
    main()