<div align="center">
  <img src="https://raw.githubusercontent.com/diusazzad/DataMind_AI/main/site/assets/images/favicon.png" alt="DataMind AI Logo" width="80" style="border-radius: 18px; margin-bottom: 10px;" onerror="this.style.display='none'"/>
  <h1>🧠 DataMind AI</h1>
  <p><strong>Enterprise Intelligent Data & Document Assistant</strong></p>
  <p>An open-source, production-ready AI platform bridging relational databases, unstructured documents, and analytical pipelines via Natural Language Text-to-SQL, source-cited RAG, and autonomous ReAct agents.</p>

  <p>
    <a href="https://datamindai.zengfy.top/"><img src="https://img.shields.io/badge/Live%20Docs-datamindai.zengfy.top-6366f1?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Live Docs"/></a>
    <a href="https://github.com/diusazzad/DataMind_AI/actions"><img src="https://img.shields.io/badge/Tests-14%2F14%20Passing-10b981?style=for-the-badge&logo=githubactions&logoColor=white" alt="CI Tests"/></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License"/></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/FastAPI-0.115+-005571?style=flat-square&logo=fastapi" alt="FastAPI"/>
    <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Versions"/>
    <img src="https://img.shields.io/badge/Zero--Trust-Strict%20Read--Only%20SQL-purple?style=flat-square&logo=shield" alt="Zero Trust"/>
    <img src="https://img.shields.io/badge/RAG-Source--Cited%20Page%20Verification-emerald?style=flat-square" alt="RAG"/>
  </p>
</div>

---

## ⚡ Live Demos & Portals

| Resource | URL | Description |
| :--- | :--- | :--- |
| 🌐 **Live Documentation Portal** | [https://datamindai.zengfy.top/](https://datamindai.zengfy.top/) | Official documentation site deployed via CI/CD. |
| 🚀 **Local Interactive Dashboard** | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Glassmorphic web UI with 4 live interactive test consoles. |
| 📘 **Swagger UI Interactive API** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | OpenAPI interactive documentation and testing suite. |
| 📗 **ReDoc Specification** | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) | Clean, responsive API specification for developers. |
| ⚡ **Telemetry Health Check** | [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health) | Real-time database connection and version telemetry. |

---

## 🌟 The 4 Architectural Pillars

```
                     ┌─────────────────────────────────────────┐
                     │          DataMind AI ReAct Agent        │
                     │         POST /api/v1/agent/chat         │
                     └────────────────────┬────────────────────┘
                                          │ Autonomous Intent Routing
             ┌────────────────────────────┼────────────────────────────┐
             ▼                            ▼                            ▼
   ┌───────────────────┐        ┌───────────────────┐        ┌───────────────────┐
   │ Safe Text-to-SQL  │        │ Document RAG      │        │ Tabular Analytics │
   │ Zero-Trust Engine │        │ Semantic Citations│        │ Profiler & Clean  │
   │ Read-Only Queries │        │ Verified Page #   │        │ Mean/Median Mode  │
   └───────────────────┘        └───────────────────┘        └───────────────────┘
```

### 1. 🤖 Autonomous ReAct AI Agent
An intelligent multi-tool orchestrator. When users ask questions in natural language, the agent autonomously identifies whether to:
- Inspect schema and execute a safe SQL database query.
- Retrieve information across indexed PDF documents with source page citations.
- Provide data profiling and statistical guidance on tabular datasets.
- Offer contextual reasoning and system explanations.

### 2. 🗄️ Zero-Trust Safe Text-to-SQL
- **Zero-Trust Guardrails:** Strict AST and regular-expression filtering blocks destructive commands: `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `GRANT`, `REVOKE`, `EXEC`.
- **Safe Bounded Returns:** Enforces a maximum 100-row fetch threshold to avoid memory denial-of-service.
- **Dynamic Introspection:** Inspects database tables and columns in real-time.

### 3. 📊 Automated Tabular Data Analytics
- **Ingestion:** Direct upload of CSV and Excel (`.xlsx`, `.xls`) files.
- **Statistical Summaries:** Computes column types, total counts, null percentages, uniqueness, mean, median, standard deviation, min, max, and correlation matrix.
- **Auto-Cleaning:** Automated duplicate row elimination and intelligent numeric/categorical null imputation (Mean, Median, Mode).

### 4. 📑 Source-Cited Document Intelligence (RAG)
- **High-Fidelity Parsing:** Extracts page-indexed text from PDF and Markdown files.
- **Semantic Vector Space:** Chunks text into overlapping semantic segments indexed via local statistical vector embeddings (zero mandatory paid API keys required).
- **Anti-Hallucination Citations:** Answers explicitly cite the primary document title, page number, and similarity relevance score.

---

## 🚀 Quickstart in 60 Seconds

### 1. Clone the Repository
```bash
git clone https://github.com/diusazzad/DataMind_AI.git
cd DataMind_AI
```

### 2. Create & Activate Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```
*(No database setup required! DataMind AI automatically initializes a local zero-config SQLite database at `sqlite:///./datamind_dev.db`)*

### 5. Launch Server
```bash
uvicorn main:app --reload --port 8000
```
Visit **[http://127.0.0.1:8000](http://127.0.0.1:8000)** to explore the interactive glassmorphic web dashboard!

---

## 🧪 Comprehensive Test Suite

Run the full automated test suite with verbose telemetry:
```bash
pytest tests -v
```

```
tests/test_agent.py::test_agent_chat_reasoning_and_capabilities PASSED   [  7%]
tests/test_agent.py::test_agent_chat_dispatches_sql_query PASSED         [ 14%]
tests/test_agent.py::test_agent_chat_dispatches_analytics_guidance PASSED [ 21%]
tests/test_analytics.py::test_profile_csv_upload PASSED                  [ 28%]
tests/test_analytics.py::test_clean_csv_upload PASSED                    [ 35%]
tests/test_health.py::test_home_portal_loads_html PASSED                 [ 42%]
tests/test_health.py::test_api_health_check PASSED                       [ 50%]
tests/test_rag.py::test_rag_upload_and_index_document PASSED             [ 57%]
tests/test_rag.py::test_rag_list_documents PASSED                        [ 64%]
tests/test_rag.py::test_rag_query_with_source_citation PASSED            [ 71%]
tests/test_rag.py::test_rag_delete_document PASSED                       [ 78%]
tests/test_sql.py::test_sql_schema_endpoint PASSED                       [ 85%]
tests/test_sql.py::test_sql_safe_query_execution PASSED                  [ 92%]
tests/test_sql.py::test_sql_forbidden_operation_blocked PASSED           [100%]

======================== 14 passed in 2.23s ========================
```

---

## 📡 API Reference & Curl Examples

### 1. Autonomous AI Agent
```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is our enterprise security policy regarding database operations?"}'
```

### 2. Execute Safe SQL Query
```bash
curl -X POST http://127.0.0.1:8000/api/v1/sql/query \
  -H "Content-Type: application/json" \
  -d '{"query_text": "SELECT 101 AS order_id, 450.75 AS total, \"Delivered\" AS status;"}'
```

### 3. Introspect Database Schema
```bash
curl -X GET http://127.0.0.1:8000/api/v1/sql/schema
```

### 4. Profile Tabular Dataset (CSV/Excel)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/analytics/profile \
  -F "file=@your_dataset.csv"
```

### 5. Automated Data Cleaning & Imputation
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/analytics/clean?drop_duplicates=true&impute_numeric=median&impute_categorical=mode" \
  -F "file=@your_dataset.csv"
```

### 6. Upload & Index Document (PDF/Markdown)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/rag/upload \
  -F "file=@company_policy.pdf"
```

### 7. Ask Document Intelligence (RAG)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What queries are forbidden under the security policy?", "top_k": 3}'
```

---

## 🛡️ Security Architecture

| Vector | Security Guardrail | Enforcement Mechanism |
| :--- | :--- | :--- |
| **SQL Injection & Mutation** | Strict Read-Only Policy | Regex & AST inspection rejects all DDL/DML mutation keywords (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `GRANT`, `REVOKE`, `EXEC`). |
| **Denial of Service (DoS)** | Bounded Row Execution | Hard query limit of 100 rows per query prevents database memory exhaustion. |
| **AI Hallucination** | Source Attribution | RAG engine strictly links synthesized statements to document titles, verified page numbers, and cosine similarity relevance metrics. |
| **File Upload Safety** | Extension & Type Validation | Whitelisted parsing for `.csv`, `.xlsx`, `.xls`, `.pdf`, `.txt`, and `.md`. |

---

## 📂 Project Structure

```
DataMind_AI/
├── .github/
│   └── workflows/
│       ├── deploy.yml            # FTP cPanel auto-deployment
│       └── test.yml              # Automated GitHub Actions Pytest CI
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── agent.py          # Unified Autonomous AI Agent
│   │   │   ├── analytics.py      # Tabular profiling & cleaning
│   │   │   ├── sql.py            # Safe Text-to-SQL endpoints
│   │   │   └── rag.py            # PDF vector indexing & Q&A
│   │   └── router.py             # Central v1 router
│   ├── core/
│   │   ├── config.py             # Pydantic BaseSettings & .env loader
│   │   └── database.py           # SQLAlchemy engine & SQLite fallback
│   ├── models/
│   │   └── schemas.py            # Pydantic DTO validation models
│   └── services/
│       ├── agent_service.py      # ReAct autonomous tool router
│       ├── data_cleaner.py       # Pandas automated cleaning engine
│       ├── document_parser.py    # PDF & text chunker with page tracking
│       ├── rag_engine.py         # Vector space indexer & citation engine
│       └── sql_engine.py         # Safe read-only SQL executor
├── static/
│   └── css/
│       └── style.css             # Glassmorphism design system & animations
├── templates/
│   └── index.html                # Interactive playground dashboard
├── tests/                        # 14 automated unit tests
├── docs/                         # MkDocs markdown documentation
├── main.py                       # FastAPI entrypoint
├── requirements.txt              # Production dependencies
├── CONTRIBUTING.md               # Git branching, PR & commit guide
└── README.md                     # Project documentation
```

---

## 🤝 Contributing
We welcome developers, researchers, and data enthusiasts to join us! Please check out our **[Contribution Guide (CONTRIBUTING.md)](CONTRIBUTING.md)** for detailed instructions on:
- Git branching conventions (`feature/`, `fix/`, `docs/`)
- Setting up your local development environment
- Commit message standards (Conventional Commits)
- Submitting Pull Requests and getting merged

---

## 📜 License
Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for complete terms.
