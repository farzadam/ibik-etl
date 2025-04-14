from pydantic import BaseModel
from typing import List, Optional, Dict

class HandleMissing(BaseModel):
    median: Optional[List[str]] = []
    most_frequent: Optional[List[str]] = []
    mean: Optional[List[str]] = []
    knn: Optional[List[str]] = []

class HandleMissing(BaseModel):
    strategies: Dict[str, List[str]] = {}

class TransformConfig(BaseModel):
    handle_missing: Optional[HandleMissing] = HandleMissing()
    remove_duplicates: bool = True
    validate_types: bool = True

class DataConfig(BaseModel):
    raw_data_dir: str
    dataset_source: str

class LoadConfig(BaseModel):
    host: str
    port: int
    dbname: str
    user: str
    password: str
    db_table: str

class ETLConfig(BaseModel):
    data: DataConfig
    transform: TransformConfig
    load: LoadConfig
