import pandas as pd
import logging
import os
from ucimlrepo import fetch_ucirepo, DatasetNotFoundError
from typing import Dict

logger = logging.getLogger(__name__)

def extract_data(data_config: Dict[str, str]) -> pd.DataFrame:
    """
    extract the Heart Disease dataset from the UCI repository using ucimlrepo.

    Args:
        data_config (dict): config dictionary with raw_data_dir key.

    Returns:
        pd.DataFrame: loaded dataset as a df.
    """
    destination_folder = data_config["raw_data_dir"]
    os.makedirs(destination_folder, exist_ok=True)

    logger.info("fetching Heart Disease Dataset from UCI repo...")
    try:
        heart_disease = fetch_ucirepo(id=45)
    except DatasetNotFoundError as e:
        logger.error(f"failed to fetch dataset {e}")
        raise

    # combine features and target into one df
    df = pd.concat([heart_disease.data.features, heart_disease.data.targets], axis=1)

    # save raw csv for reference
    raw_csv_path = os.path.join(destination_folder, "heart_disease.csv")
    df.index.name = "id"
    df.to_csv(raw_csv_path, index=True)
    logger.info(f"saved dataset to {raw_csv_path}")

    return df
