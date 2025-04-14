import pandas as pd
from sqlalchemy import create_engine, URL
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def load_data(df: pd.DataFrame, load_config: Dict[str, str]) -> None:
    """
    loads the transformed df into postgres.

    Args:
        df (pd.DataFrame): data.
        load_config (dict):  db connection details and target table name.
    """
    db_url = URL.create(
        "postgresql",
        username=load_config['user'],
        password=load_config['password'],
        host=load_config['host'],
        port=load_config['port'],
        database=load_config['dbname'] ,
        )

    try:
        engine = create_engine(db_url)
        df.to_sql(load_config["db_table"], engine, if_exists="replace", index=True)
        logger.info(f"successfully loaded data into table '{load_config['db_table']}'.")
    except OperationalError as conn_err:
        logger.error(f"Database connection failed: {conn_err}")
        raise
    except SQLAlchemyError as db_err:
        logger.error(f"SQLAlchemy error while loading data: {db_err}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading data into PostgreSQL: {e}")
        raise
