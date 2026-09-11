# 🤝 Contributing to DataMind AI

Thank you for your interest in contributing to **DataMind AI**! Whether you are fixing a bug, designing a new feature, improving documentation, or adding automated tests, your help is deeply appreciated.

---

## 📋 Table of Contents
1. [Code of Conduct](#-code-of-conduct)
2. [Getting Started & Local Environment Setup](#-getting-started--local-environment-setup)
3. [Git Branching Guidelines](#-git-branching-guidelines)
4. [Development Standards & Best Practices](#-development-standards--best-practices)
5. [Automated Testing](#-automated-testing)
6. [Commit Message Conventions](#-commit-message-conventions)
7. [Submitting a Pull Request (PR)](#-submitting-a-pull-request-pr)
8. [Community & Questions](#-community--questions)

---

## 📜 Code of Conduct
We are committed to providing a welcoming, diverse, and harassment-free environment. Please treat all maintainers and fellow contributors with respect, empathy, and professional courtesy. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for full details.

---

## 🚀 Getting Started & Local Environment Setup

### 1. Fork the Repository
Click the **Fork** button at the top-right of the [DataMind AI GitHub Repository](https://github.com/diusazzad/DataMind_AI) to create your own copy under your GitHub account.

### 2. Clone Your Fork
Clone your fork to your local development machine:
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/DataMind_AI.git
cd DataMind_AI
```

### 3. Set Up Upstream Remote
Configure Git to track the official repository as `upstream`:
```bash
git remote add upstream https://github.com/diusazzad/DataMind_AI.git
git fetch upstream
```

### 4. Create a Virtual Environment
We recommend Python 3.10 through 3.13:

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

### 5. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Configure Environment Variables
Copy the template `.env.example`:
```bash
cp .env.example .env
```
*(By default, DataMind AI operates seamlessly with zero configuration by automatically initializing a local SQLite database at `sqlite:///./datamind_dev.db`)*

### 7. Run the Local Development Server
```bash
uvicorn main:app --reload --port 8000
```
- 🌐 Web Dashboard: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 📘 Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📗 ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🌿 Git Branching Guidelines

Never commit directly to the `main` branch. Always create a dedicated branch for your work branching off the latest `upstream/main`:

```bash
git checkout main
git pull upstream main
git checkout -b <branch-type>/<short-description>
```

### Branch Naming Conventions:
Use clear, prefix-based branch names:

| Branch Type | Purpose | Example |
| :--- | :--- | :--- |
| `feature/` | New features or engine expansions | `feature/langchain-react-memory` |
| `fix/` | Bug fixes or guardrail patches | `fix/sqlite-timeout-exception` |
| `docs/` | Documentation, PRD, or guide updates | `docs/api-curl-examples` |
| `test/` | Adding or refactoring unit/integration tests | `test/rag-citation-edge-cases` |
| `refactor/` | Code structure improvements without feature changes | `refactor/sql-engine-service` |
| `chore/` | Tooling, dependencies, or GitHub Actions CI | `chore/update-fastapi-version` |

---

## 🛠️ Development Standards & Best Practices

1. **Architecture Layering:**
   - **Routes & Controllers:** Keep inside `app/api/v1/`. Routes should strictly validate requests and delegate heavy logic to services.
   - **Services & Core Engines:** Business logic, RAG pipelines, data profiling, and SQL executors reside inside `app/services/`.
   - **Schemas:** All DTOs, request payloads, and response structures must be defined with Pydantic in `app/models/schemas.py`.
2. **Zero-Trust Security Principles:**
   - Any feature dealing with database execution must strictly adhere to the Read-Only validation rules in `app/services/sql_engine.py`.
   - Never allow unbounded memory allocations or un-sanitized file uploads.
3. **PEP 8 & Formatting:**
   - Code must follow standard PEP 8 formatting rules.
   - Use meaningful variable and function names.
   - Include docstrings for public classes and service methods.

---

## 🧪 Automated Testing

We enforce a strict testing policy. All pull requests must pass the automated test suite.

### Running Tests Locally:
```bash
pytest tests -v
```

### Adding New Tests:
- If you add a new endpoint or service, create corresponding tests in the `tests/` directory (e.g., `tests/test_new_feature.py`).
- Use `fastapi.testclient.TestClient` for HTTP API testing.
- Verify both the **happy path** and **error edge cases** (such as blocked unauthorized SQL queries or invalid file formats).

---

## 💬 Commit Message Conventions

We follow the **Conventional Commits** specification:

```
<type>(<scope>): <short description in present tense>
```

### Allowed Types:
- `feat`: A new feature (e.g., `feat(agent): add multi-turn conversation memory`)
- `fix`: A bug fix (e.g., `fix(sql): prevent multi-statement injection bypass`)
- `docs`: Documentation changes only (e.g., `docs(readme): add docker deployment section`)
- `test`: Adding or correcting tests (e.g., `test(analytics): add excel null imputation test`)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `chore`: Updates to build tasks, package manager configs, etc.

---

## 📬 Submitting a Pull Request (PR)

### 1. Rebase from Upstream Main
Before submitting, ensure your branch is cleanly rebased on top of the latest `upstream/main`:
```bash
git checkout main
git pull upstream main
git checkout your-feature-branch
git rebase main
```

### 2. Push to Your Fork
```bash
git push -u origin your-feature-branch
```

### 3. Open the Pull Request on GitHub
1. Navigate to [https://github.com/diusazzad/DataMind_AI](https://github.com/diusazzad/DataMind_AI).
2. Click the green **Compare & pull request** button.
3. Fill in the **PR Template** accurately:
   - Reference the Issue number it resolves (e.g., `Fixes #12`).
   - Describe what changed and why.
   - Confirm all local automated tests passed.
   - Provide screenshots if your changes affect the Web UI (`templates/index.html` or `static/css/style.css`).
4. Click **Create Pull Request**.

### 4. Review Process
- The automated GitHub Actions CI pipeline will automatically run `pytest` against your code.
- Maintainers will review your PR, suggest improvements if needed, and merge it upon approval.

---

## 🌟 Community & Questions

- **Found a bug?** Open an issue on our [Issue Tracker](https://github.com/diusazzad/DataMind_AI/issues).
- **Have an idea or architectural suggestion?** Start a discussion or open a draft PR.

Thank you for helping make **DataMind AI** the premier open-source Intelligent Data & Document Assistant! 🚀
