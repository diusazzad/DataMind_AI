# Project Setup & Packages Guide

This document tracks all the packages and configurations used from the beginning of the project to help new contributors get started quickly.

## 1. Virtual Environment Setup
To keep our dependencies isolated, we created a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

## 2. Core Dependencies
We installed the foundational packages for Phase 1 (Data Analysis & API):
```bash
pip install fastapi uvicorn pandas numpy sqlalchemy matplotlib psycopg2-binary
```
- **fastapi & uvicorn**: For building and running the high-performance API backend.
- **pandas & numpy**: For robust data cleaning, manipulation, and statistical operations.
- **sqlalchemy & psycopg2-binary**: For connecting and interacting with the PostgreSQL database.

## 3. Auto-Reload Fix (Windows)
To ensure Uvicorn auto-reloads correctly on Windows file changes, we added watchfiles:
```bash
pip install watchfiles
```

## 4. Documentation Site
To build this beautiful documentation landing page, we use MkDocs with the Material theme:
```bash
pip install mkdocs-material
```
