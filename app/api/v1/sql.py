import re
from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.models.schemas import SqlQueryRequest, SqlQueryResponse
from app.services.sql_engine import SqlEngineService

router = APIRouter(prefix="/sql", tags=["Text-to-SQL Engine"])


@router.get("/schema", response_model=Dict[str, List[str]])
def get_database_schema():
    """Returns all tables and their respective columns from the connected database."""
    try:
        return SqlEngineService.get_database_schema()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schema inspection failed: {str(e)}")


@router.post("/query", response_model=SqlQueryResponse)
def execute_sql_query(request: SqlQueryRequest):
    """Executes a SQL query in strict Read-Only mode, or converts a natural prompt into SQL."""
    raw_query = request.query_text.strip()
    
    # Check if query contains explicit SQL clauses or forbidden operators
    is_explicit_sql = any(
        re.search(rf"\b{kw}\b", raw_query, re.IGNORECASE)
        for kw in ["SELECT", "WITH", "EXPLAIN"] + SqlEngineService.FORBIDDEN_KEYWORDS
    )

    if is_explicit_sql:
        try:
            SqlEngineService.validate_safety(raw_query)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        query = raw_query
    else:
        # Natural language prompt
        schema = SqlEngineService.get_database_schema()
        query = SqlEngineService.generate_sql_from_prompt(raw_query, schema)

    try:
        return SqlEngineService.execute_query(query)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database execution error: {str(e)}")
