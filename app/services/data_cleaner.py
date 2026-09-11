import io
from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from app.models.schemas import (
    ColumnProfile,
    DataCleanOptions,
    DataCleanResponse,
    DataProfileResponse,
)


class DataCleanerService:
    @staticmethod
    def read_file(file_content: bytes, filename: str) -> pd.DataFrame:
        """Parses CSV, TSV, or Excel files into a Pandas DataFrame."""
        lower_name = filename.lower()
        if lower_name.endswith(('.csv', '.txt')):
            # Try utf-8 first, fallback to latin-1
            try:
                return pd.read_csv(io.BytesIO(file_content))
            except UnicodeDecodeError:
                return pd.read_csv(io.BytesIO(file_content), encoding="latin1")
        elif lower_name.endswith(('.xlsx', '.xls')):
            return pd.read_excel(io.BytesIO(file_content))
        else:
            raise ValueError(f"Unsupported file format: {filename}. Please upload CSV or Excel.")

    @classmethod
    def generate_profile(cls, df: pd.DataFrame, filename: str) -> DataProfileResponse:
        """Computes descriptive statistics, missing counts, and distribution metrics."""
        total_rows, total_columns = df.shape
        columns_profile: List[ColumnProfile] = []

        for col in df.columns:
            series = df[col]
            null_count = int(series.isnull().sum())
            null_pct = round((null_count / total_rows * 100) if total_rows > 0 else 0.0, 2)
            unique_count = int(series.nunique(dropna=True))
            dtype = str(series.dtype)

            mean_val = None
            std_val = None
            min_val = None
            max_val = None

            if pd.api.types.is_numeric_dtype(series):
                cleaned_numeric = series.dropna()
                if not cleaned_numeric.empty:
                    mean_val = round(float(cleaned_numeric.mean()), 3)
                    std_val = round(float(cleaned_numeric.std()), 3) if len(cleaned_numeric) > 1 else 0.0
                    min_val = float(cleaned_numeric.min())
                    max_val = float(cleaned_numeric.max())
            elif pd.api.types.is_datetime64_any_dtype(series):
                cleaned_dates = series.dropna()
                if not cleaned_dates.empty:
                    min_val = str(cleaned_dates.min())
                    max_val = str(cleaned_dates.max())
            else:
                cleaned_str = series.dropna()
                if not cleaned_str.empty:
                    min_val = str(cleaned_str.min())[:50]
                    max_val = str(cleaned_str.max())[:50]

            sample_vals = [
                None if pd.isna(v) else (float(v) if isinstance(v, (np.floating, float)) else str(v))
                for v in series.head(5).tolist()
            ]

            columns_profile.append(
                ColumnProfile(
                    name=str(col),
                    dtype=dtype,
                    total_count=total_rows,
                    null_count=null_count,
                    null_percentage=null_pct,
                    unique_count=unique_count,
                    mean=mean_val,
                    std=std_val,
                    min=min_val,
                    max=max_val,
                    sample_values=sample_vals,
                )
            )

        # Correlation matrix for numeric fields
        correlations: Dict[str, Dict[str, float]] = {}
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty and numeric_df.shape[1] > 1:
            corr_matrix = numeric_df.corr().round(3)
            for c1 in corr_matrix.columns:
                correlations[c1] = {}
                for c2 in corr_matrix.index:
                    val = corr_matrix.loc[c2, c1]
                    correlations[c1][c2] = float(val) if not pd.isna(val) else 0.0

        preview = df.head(10).replace({np.nan: None}).to_dict(orient="records")

        return DataProfileResponse(
            file_name=filename,
            total_rows=total_rows,
            total_columns=total_columns,
            columns=columns_profile,
            preview=preview,
            correlations=correlations or None,
        )

    @classmethod
    def clean_data(cls, df: pd.DataFrame, options: DataCleanOptions) -> Tuple[pd.DataFrame, DataCleanResponse]:
        """Cleans dataset according to configured options."""
        initial_rows = len(df)
        initial_nulls = int(df.isnull().sum().sum())
        working_df = df.copy()

        duplicates_removed = 0
        if options.drop_duplicates:
            before_dup = len(working_df)
            working_df = working_df.drop_duplicates()
            duplicates_removed = before_dup - len(working_df)

        # Impute numeric columns
        if options.impute_numeric in ["mean", "median"]:
            for col in working_df.select_dtypes(include=[np.number]).columns:
                if working_df[col].isnull().any():
                    if options.impute_numeric == "mean":
                        fill_val = working_df[col].mean()
                    else:
                        fill_val = working_df[col].median()
                    working_df[col] = working_df[col].fillna(fill_val)

        # Impute categorical columns
        if options.impute_categorical == "mode":
            for col in working_df.select_dtypes(exclude=[np.number]).columns:
                if working_df[col].isnull().any():
                    modes = working_df[col].mode()
                    fill_val = modes.iloc[0] if not modes.empty else "Unknown"
                    working_df[col] = working_df[col].fillna(fill_val)

        remaining_nulls = int(working_df.isnull().sum().sum())
        cleaned_rows = len(working_df)
        preview = working_df.head(10).replace({np.nan: None}).to_dict(orient="records")

        response = DataCleanResponse(
            success=True,
            initial_rows=initial_rows,
            cleaned_rows=cleaned_rows,
            initial_nulls=initial_nulls,
            remaining_nulls=remaining_nulls,
            duplicates_removed=duplicates_removed,
            preview=preview,
        )

        return working_df, response
