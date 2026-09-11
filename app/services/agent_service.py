import time
import re
from typing import Any, Dict, List, Optional
from app.services.sql_engine import sql_engine
from app.services.rag_engine import rag_engine
from app.models.schemas import (
    AgentChatRequest,
    AgentChatResponse,
    RagCitation,
)


class AgentService:
    """
    Autonomous ReAct AI Agent capable of tool routing across:
    1. SQL Database Inspection & Execution
    2. RAG Document Intelligence with Source Citations
    3. Tabular Data Analytics Guidance
    4. General Natural Language Reasoning
    """

    def __init__(self):
        pass

    def _detect_intent(self, message: str) -> str:
        msg = message.strip().lower()

        # Check for explicit or implicit SQL requests
        if msg.startswith("select ") or "from " in msg or "database" in msg or "table" in msg or "sql" in msg:
            return "sql"

        # Check for data analytics / statistics keywords
        if any(w in msg for w in ["profile", "dataset", "dataframe", "correlation", "null count", "clean data", "impute", "mean", "median"]):
            return "analytics"

        # Check for document / policy / manual keywords or question forms
        if any(w in msg for w in ["document", "policy", "pdf", "manual", "security", "architecture", "what is", "explain", "how to"]):
            # If documents exist in RAG engine, RAG is primary candidate
            if rag_engine.list_documents():
                return "rag"
            else:
                return "reasoning"

        return "reasoning"

    def process_chat(self, request: AgentChatRequest) -> AgentChatResponse:
        start_time = time.time()
        user_msg = request.message.strip()
        intent = self._detect_intent(user_msg)

        tool_used = None
        tool_output: Optional[Dict[str, Any]] = None
        citations: Optional[List[RagCitation]] = None
        reply = ""

        if intent == "sql":
            tool_used = "safe_sql_engine"
            try:
                # If it looks like a natural language question about tables, generate safe SQL
                if not user_msg.lower().startswith("select"):
                    sql_query = sql_engine.generate_sql_from_prompt(user_msg)
                else:
                    sql_query = user_msg

                res = sql_engine.execute_query(sql_query)
                tool_output = {
                    "sql": res.sql,
                    "row_count": res.row_count,
                    "columns": res.columns,
                    "results": res.results[:10]  # top 10 preview
                }
                reply = (
                    f"I queried the database using the safe SQL protocol:\n"
                    f"`{res.sql}`\n\n"
                    f"**Result Summary:** Retrieved {res.row_count} row(s).\n"
                    f"{res.explanation}"
                )
            except Exception as e:
                reply = f"I attempted to query the database, but encountered a security or execution notice: {str(e)}"
                tool_output = {"error": str(e)}

        elif intent == "rag":
            tool_used = "rag_document_intelligence"
            rag_res = rag_engine.query_documents(user_msg, top_k=3)
            tool_output = {
                "retrieved_chunks": rag_res.retrieved_chunks_count,
                "citations_count": len(rag_res.citations)
            }
            citations = rag_res.citations
            reply = rag_res.answer

        elif intent == "analytics":
            tool_used = "data_analytics_pipeline"
            reply = (
                "DataMind AI's automated Data Analytics pipeline can ingest your CSV or Excel files, "
                "calculate full descriptive statistics (mean, median, standard deviation, skewness), "
                "detect missing values, generate correlation matrices, and handle null value imputation. "
                "You can test this anytime in the 'Analytics Profiler' tab or via `POST /api/v1/analytics/profile`."
            )
            tool_output = {
                "supported_formats": ["CSV", "Excel (.xlsx)"],
                "features": ["Descriptive Statistics", "Null Imputation", "Correlation Matrix", "Duplicate Removal"]
            }

        else:
            intent = "reasoning"
            # Conversational / Assistant guidance
            docs_count = len(rag_engine.list_documents())
            reply = (
                f"Hello! I am DataMind AI — your unified Enterprise Intelligent Data & Document Assistant.\n\n"
                f"Here is what I can do for you autonomously:\n"
                f"1. **🗄️ Database & Text-to-SQL:** Ask natural language questions or run read-only SQL queries with built-in zero-trust security guardrails.\n"
                f"2. **📑 Document Intelligence (RAG):** Ask questions across uploaded PDF and markdown documents with verified document & page citations (Currently {docs_count} indexed).\n"
                f"3. **📊 Tabular Data Analytics:** Ingest and profile datasets with automated null-imputation and distribution metrics.\n\n"
                f"Feel free to ask a database query, upload a policy document, or ask me anything!"
            )

        latency = round((time.time() - start_time) * 1000, 2)
        return AgentChatResponse(
            reply=reply,
            intent=intent,
            tool_used=tool_used,
            tool_output=tool_output,
            citations=citations,
            latency_ms=latency
        )


agent_service = AgentService()
