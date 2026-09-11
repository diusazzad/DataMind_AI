from fastapi import APIRouter
from app.api.v1.analytics import router as analytics_router
from app.api.v1.sql import router as sql_router
from app.api.v1.rag import router as rag_router
from app.api.v1.agent import router as agent_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(analytics_router)
api_v1_router.include_router(sql_router)
api_v1_router.include_router(rag_router)
api_v1_router.include_router(agent_router)


