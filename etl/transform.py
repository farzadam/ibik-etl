import pandas as pd
import pandera as pa

import logging
from typing import Dict, List
from sklearn.impute import SimpleImputer, KNNImputer
from etl.schema import schema


logger = logging.getLogger(__name__)


def transform_data(df: pd.DataFrame, transform_cfg: Dict) -> pd.DataFrame:
    """
    clean the dataset by handling missing values, removing duplicates, and validating data types.

    Args:
        df (pd.DataFrame): input raw df.
        transform_cfg (Dict): config for transformation steps.

    Returns:
        pd.DataFrame: cleaned and transformed df.
    """
    df_clean = df.copy()

    ## transformation steps:
    # 1. type validation
    if transform_cfg.get("validate_types", True):
        try:
            schema.validate(df_clean)
            logger.info(f"dataset schema validated.")
        except pa.errors.SchemaError as exc:
            logger.error(f"schema validation failed: {exc}")
            raise

    # 2. handle missing values
    missing_cfg = transform_cfg.get("handle_missing", {})
    strategy_cfg: Dict[str, List[str]] = missing_cfg.get("strategies", {})

    # 2.1 simple strategies (mean, median, mode)
    for strategy, columns in strategy_cfg.items():
        if not columns:
            continue

        imputer = SimpleImputer(strategy=strategy, add_indicator=True)
        imputed = imputer.fit_transform(df_clean[columns])

        output_cols = imputer.get_feature_names_out(columns)
        df_imputed = pd.DataFrame(imputed, columns=output_cols, index=df_clean.index)

        df_clean = df_clean.drop(columns=columns)
        df_clean = pd.concat([df_clean, df_imputed], axis=1)

        # log imputations per column
        for col in columns:
            indicator_col = f"missingindicator_{col}"
            if indicator_col in df_imputed.columns:
                n_missing = int(df_imputed[indicator_col].sum())
                logger.info(f"imputed {n_missing} values in column '{col}' using strategy '{strategy}'.")

    # 2.2 KNN imputation
    knn_cols = strategy_cfg.get("knn", [])
    if knn_cols:
        imputer = KNNImputer(n_neighbors=5)
        knn_imputed = imputer.fit_transform(df_clean[knn_cols])
        df_clean[knn_cols] = knn_imputed
        logger.info(f"applied KNN imputation on columns: {knn_cols}")

    # 3. deduplication
    if transform_cfg.get("remove_duplicates", True):
        before = len(df_clean)
        df_clean.drop_duplicates(inplace=True)
        after = len(df_clean)
        logger.info(f"removed {before - after} duplicate rows.")


    return df_clean
