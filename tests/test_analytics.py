import io
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

SAMPLE_CSV = """id,name,age,salary,department
1,Alice,29,75000,Engineering
2,Bob,,82000,Marketing
3,Charlie,35,90000,Engineering
4,Diana,28,,Sales
5,Eve,42,120000,Management
5,Eve,42,120000,Management
"""


def test_profile_csv_upload():
    csv_file = io.BytesIO(SAMPLE_CSV.encode("utf-8"))
    response = client.post(
        "/api/v1/analytics/profile",
        files={"file": ("employees.csv", csv_file, "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["file_name"] == "employees.csv"
    assert data["total_rows"] == 6
    assert data["total_columns"] == 5
    
    col_names = [c["name"] for c in data["columns"]]
    assert "age" in col_names
    assert "salary" in col_names

    # Check that age has 1 null value
    age_col = next(c for c in data["columns"] if c["name"] == "age")
    assert age_col["null_count"] == 1


def test_clean_csv_upload():
    csv_file = io.BytesIO(SAMPLE_CSV.encode("utf-8"))
    response = client.post(
        "/api/v1/analytics/clean?drop_duplicates=true&impute_numeric=median",
        files={"file": ("employees.csv", csv_file, "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["duplicates_removed"] == 1
    assert data["cleaned_rows"] == 5
    assert data["remaining_nulls"] == 0
