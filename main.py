from fastapi import FastAPI

app = FastAPI(
    title="DataMind AI API",
    description="Intelligent Data & Document Assistant API",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {"Status": "success", "message": "DataMind AI Server is running flawlessly!!!!"}
 