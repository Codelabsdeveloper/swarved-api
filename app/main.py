from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.utils.logger import get_logger
from app.models.schemas import QueryRequest, QueryResponse, HealthResponse
from app.services.rag_pipeline import get_rag_pipeline
from app.services.vector_db import get_vector_db

logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RAG Backend for Document Question Answering",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    try:
        get_rag_pipeline()
        logger.info("RAG pipeline initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG pipeline: {e}")


@app.get("/", tags=["System"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    vector_db = get_vector_db()
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        qdrant_connected=vector_db.health_check(),
        documents_indexed=vector_db.count_documents(),
    )


@app.post("/query", response_model=QueryResponse, tags=["RAG"])
async def process_query(request: QueryRequest):
    try:
        logger.info(f"Received query: {request.message[:100]}...")
        rag_pipeline = get_rag_pipeline()
        response = rag_pipeline.process_query(request)
        return response
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
