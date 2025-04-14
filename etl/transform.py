import pandas as pd
import pandera as pa
import logging
from typing import Dict, List
from sklearn.impute import SimpleImputer, KNNImputer
from pandera import Column, DataFrameSchema, Check


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define dataset schema based on observed values
schema = DataFrameSchema({
    "age": Column(pa.Int, Check.in_range(1, 120)),
    "sex": Column(pa.Int, Check.isin([0, 1])),
    "cp": Column(pa.Int, Check.isin([1, 2, 3, 4])),
    "trestbps": Column(pa.Int, Check.in_range(10, 300)),
    "chol": Column(pa.Int, Check.in_range(100, 600)),
    "fbs": Column(pa.Int, Check.isin([0, 1])),
    "restecg": Column(pa.Int, Check.isin([0, 1, 2])),
    "thalach": Column(pa.Int, Check.in_range(50, 250)),
    "exang": Column(pa.Int, Check.isin([0, 1])),
    "oldpeak": Column(pa.Float, Check.ge(0.0)),
    "slope": Column(pa.Int, Check.isin([1, 2, 3])),
    "ca": Column(pa.Float, Check.isin([0, 1, 2, 3]), nullable=True),
    "thal": Column(pa.Float, Check.isin([3, 6, 7]), nullable=True),
    "num": Column(pa.Int, Check.isin([0, 1, 2, 3, 4])),
})


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
    # 1. handle missing values
    missing_cfg = transform_cfg.get("handle_missing", {})
    strategy_cfg: Dict[str, List[str]] = missing_cfg.get("strategies", {})

    # 1.1 simple strategies (mean, median, mode)
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

    # 1.2 KNN imputation
    knn_cols = strategy_cfg.get("knn", [])
    if knn_cols:
        imputer = KNNImputer(n_neighbors=5)
        knn_imputed = imputer.fit_transform(df_clean[knn_cols])
        df_clean[knn_cols] = knn_imputed
        logger.info(f"applied KNN imputation on columns: {knn_cols}")

    # 2. deduplication
    if transform_cfg.get("remove_duplicates", True):
        before = len(df_clean)
        df_clean.drop_duplicates(inplace=True)
        after = len(df_clean)
        logger.info(f"removed {before - after} duplicate rows.")

    # 3. type validation
    if transform_cfg.get("validate_types", True):
        schema.validate(df_clean)
        logger.info(f"types validated.")


    return df_clean
