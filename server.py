import uvicorn
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info(f"Starting {settings.APP_NAME} server")
    logger.info(f"Host: {settings.HOST}")
    logger.info(f"Port: {settings.PORT}")
    logger.info(f"Debug: {settings.DEBUG}")

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )


if __name__ == "__main__":
    main()