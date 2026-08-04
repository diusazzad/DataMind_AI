<div align="center">
  <h1>🚀 DataMind AI</h1>
  <p><strong>Intelligent Data & Document Assistant</strong></p>
  <p>DataMind AI is an open-source AI platform that empowers users to analyze tabular data, chat with their databases via Text-to-SQL, and extract insights from documents using RAG (Retrieval-Augmented Generation).</p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
  [![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
</div>

## 🌟 Features

- **Data Analytics Pipeline:** Upload CSV/Excel files and instantly get cleaned data and statistical insights.
- **Text-to-SQL (AI Agents):** Ask questions in natural language, and the AI will generate and execute SQL queries on your PostgreSQL database securely.
- **Document Intelligence (RAG):** Upload PDFs and chat with your documents. Get highly accurate answers backed by source citations to prevent hallucinations.
- **Modern API Backend:** Built on high-performance FastAPI.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Data Science:** Pandas, Numpy, Scikit-Learn
- **AI & LLM:** OpenAI, LangChain, ChromaDB (Vector Store)
- **Database:** PostgreSQL

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL
- OpenAI API Key

### Installation

1. **Fork and Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/DataMind_AI.git
   cd DataMind_AI
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy the `.env.example` file to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```

5. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
   Access the API documentation at `http://127.0.0.1:8000/docs`.

## 🤝 Contributing
We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and our coding standards.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
