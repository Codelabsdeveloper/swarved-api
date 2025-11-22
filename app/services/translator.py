from typing import Optional
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class TranslationService:
    def __init__(self):
        self.supported_languages = settings.SUPPORTED_LANGUAGES
        self.default_language = settings.DEFAULT_LANGUAGE

    def translate(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ) -> str:
        if target_language not in self.supported_languages:
            logger.warning(f"Unsupported language: {target_language}")
            return text

        if target_language == "en" or target_language == source_language:
            return text

        logger.info(f"Translation requested: {source_language} -> {target_language}")
        logger.warning("Translation not implemented yet, returning original text")

        return text

    def detect_language(self, text: str) -> str:
        try:
            from langdetect import detect

            lang = detect(text)
            logger.debug(f"Detected language: {lang}")
            return lang
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return self.default_language

_translation_service_instance = None

def get_translation_service() -> TranslationService:
    global _translation_service_instance
    if _translation_service_instance is None:
        _translation_service_instance = TranslationService()
    return _translation_service_instance