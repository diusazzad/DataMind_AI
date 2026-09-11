from fastapi import APIRouter, File, HTTPException, UploadFile
from app.models.schemas import DataCleanOptions, DataCleanResponse, DataProfileResponse
from app.services.data_cleaner import DataCleanerService

router = APIRouter(prefix="/analytics", tags=["Data Analytics Pipeline"])


@router.post("/profile", response_model=DataProfileResponse)
async def profile_uploaded_file(file: UploadFile = File(...)):
    """Upload a CSV or Excel file and instantly get statistical summaries, data types, and correlation metrics."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="A valid file with a filename must be provided.")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    try:
        df = DataCleanerService.read_file(content, file.filename)
        profile = DataCleanerService.generate_profile(df, file.filename)
        return profile
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to profile dataset: {str(e)}")


@router.post("/clean", response_model=DataCleanResponse)
async def clean_uploaded_file(
    file: UploadFile = File(...),
    drop_duplicates: bool = True,
    impute_numeric: str = "median",
    impute_categorical: str = "mode"
):
    """Automatically clean an uploaded dataset by removing duplicates and imputing missing values."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="A valid file must be provided.")

    content = await file.read()
    try:
        df = DataCleanerService.read_file(content, file.filename)
        options = DataCleanOptions(
            drop_duplicates=drop_duplicates,
            impute_numeric=impute_numeric,
            impute_categorical=impute_categorical
        )
        _, clean_response = DataCleanerService.clean_data(df, options)
        return clean_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clean dataset: {str(e)}")
