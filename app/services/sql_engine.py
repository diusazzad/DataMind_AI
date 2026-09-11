import re
import time
from typing import Any, Dict, List, Optional
from sqlalchemy import inspect, text

from app.core.database import engine
from app.models.schemas import SqlQueryResponse


class SqlEngineService:
    FORBIDDEN_KEYWORDS = [
        "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE",
        "GRANT", "REVOKE", "EXEC", "EXECUTE", "CREATE", "REPLACE"
    ]

    @classmethod
    def get_database_schema(cls) -> Dict[str, List[str]]:
        """Introspects tables and column names from the active database."""
        inspector = inspect(engine)
        schema: Dict[str, List[str]] = {}
        for table_name in inspector.get_table_names():
            columns = [col["name"] for col in inspector.get_columns(table_name)]
            schema[table_name] = columns
        return schema

    @classmethod
    def validate_safety(cls, sql_query: str) -> None:
        """Enforces strictly read-only execution."""
        clean_sql = re.sub(r"--.*?$|\/\*.*?\*\/", "", sql_query, flags=re.MULTILINE).strip().upper()
        
        for keyword in cls.FORBIDDEN_KEYWORDS:
            pattern = rf"\b{keyword}\b"
            if re.search(pattern, clean_sql):
                raise ValueError(
                    f"Security Exception: Operation '{keyword}' is forbidden. DataMind AI operates in strict Read-Only mode."
                )

        if not clean_sql.startswith("SELECT") and not clean_sql.startswith("WITH") and not clean_sql.startswith("EXPLAIN"):
            raise ValueError("Security Exception: Only SELECT queries are permitted.")

    @classmethod
    def execute_query(cls, sql_query: str) -> SqlQueryResponse:
        """Validates and executes a SQL query safely, returning tabular data and execution metrics."""
        cls.validate_safety(sql_query)

        start_time = time.perf_counter()
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            columns = list(result.keys())
            rows = result.fetchmany(100)  # Safe bounded fetch limit

            results: List[Dict[str, Any]] = [
                {col: val for col, val in zip(columns, row)}
                for row in rows
            ]
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        explanation = (
            f"Successfully executed query against database. Retrieved {len(results)} records "
            f"across {len(columns)} fields in {elapsed_ms}ms."
        )

        return SqlQueryResponse(
            success=True,
            sql=sql_query,
            explanation=explanation,
            row_count=len(results),
            columns=columns,
            results=results,
            execution_time_ms=elapsed_ms,
        )

    @classmethod
    def generate_sql_from_prompt(cls, prompt: str, schema: Optional[Dict[str, List[str]]] = None) -> str:
        """Rule-based and template generator for natural queries when LLM key is absent."""
        if schema is None:
            schema = cls.get_database_schema()
        prompt_lower = prompt.lower()

        # Find best matching table
        matched_table = None
        for table in schema.keys():
            if table.lower() in prompt_lower:
                matched_table = table
                break

        if not matched_table and schema:
            matched_table = list(schema.keys())[0]

        if not matched_table:
            # Demonstration table if schema is currently empty
            return "SELECT 1 AS status, 'No tables found in database' AS message;"

        # Count query
        if "how many" in prompt_lower or "count" in prompt_lower:
            return f"SELECT COUNT(*) AS total_count FROM {matched_table};"

        # Limit queries
        limit_match = re.search(r"top\s+(\d+)|first\s+(\d+)|limit\s+(\d+)", prompt_lower)
        limit_val = limit_match.group(1) or limit_match.group(2) or limit_match.group(3) if limit_match else 10

        return f"SELECT * FROM {matched_table} LIMIT {limit_val};"


sql_engine = SqlEngineService

