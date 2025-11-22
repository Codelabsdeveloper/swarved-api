from pathlib import Path
from app.config import settings
from app.services.ingestion import get_ingestion_service
from app.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    documents_dir = settings.DOCUMENTS_DIR
    ingestion_service = get_ingestion_service()
    results = ingestion_service.ingest_directory(documents_dir)


if __name__ == "__main__":
    main()