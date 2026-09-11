from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    database_connected: bool


class ColumnProfile(BaseModel):
    name: str
    dtype: str
    total_count: int
    null_count: int
    null_percentage: float
    unique_count: int
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[Any] = None
    max: Optional[Any] = None
    sample_values: List[Any] = []


class DataProfileResponse(BaseModel):
    file_name: str
    total_rows: int
    total_columns: int
    columns: List[ColumnProfile]
    preview: List[Dict[str, Any]]
    correlations: Optional[Dict[str, Dict[str, float]]] = None


class DataCleanOptions(BaseModel):
    drop_duplicates: bool = True
    impute_numeric: str = Field(default="median", description="none, mean, or median")
    impute_categorical: str = Field(default="mode", description="none or mode")
    fill_value: Optional[str] = None


class DataCleanResponse(BaseModel):
    success: bool
    initial_rows: int
    cleaned_rows: int
    initial_nulls: int
    remaining_nulls: int
    duplicates_removed: int
    preview: List[Dict[str, Any]]


class SqlQueryRequest(BaseModel):
    query_text: str = Field(..., description="Natural language question or direct SQL")
    table_name: Optional[str] = None


class SqlQueryResponse(BaseModel):
    success: bool
    sql: str
    explanation: str
    row_count: int
    columns: List[str]
    results: List[Dict[str, Any]]
    execution_time_ms: float
