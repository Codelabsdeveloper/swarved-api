import os
import subprocess
from pathlib import Path
from typing import Optional
from docx import Document
from app.utils.logger import get_logger

logger = get_logger(__name__)


def read_text_file(file_path: Path) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading text file {file_path}: {e}")
        return ""


def read_pdf_file(file_path: Path) -> str:
    try:
        try:
            import PyPDF2

            text = ""
            with open(file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"

            return text
        except ImportError:
            logger.warning("PyPDF2 not installed. Install with: pip install PyPDF2")
            return ""

    except Exception as e:
        logger.error(f"Error reading PDF file {file_path}: {e}")
        return ""


def read_doc_file(file_path: Path) -> str:
    try:
        result = subprocess.run(
            ['antiword', '-w', '0', str(file_path)],
            capture_output=True,
            timeout=60
        )
        
        if result.returncode == 0:
            text = ""
            for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    text = result.stdout.decode(encoding, errors='ignore')
                    if text:
                        break
                except:
                    continue
            return text
        else:
            logger.error(f"antiword failed for {file_path}")
            return ""
    except FileNotFoundError:
        logger.error("antiword not installed. Install with: brew install antiword")
        return ""
    except Exception as e:
        logger.error(f"Error reading DOC file {file_path}: {e}")
        return ""


def read_docx_file(file_path: Path) -> str:
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        logger.error(f"Error reading DOCX file {file_path}: {e}")
        return ""


def read_document(file_path: Path) -> Optional[str]:
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return None

    extension = file_path.suffix.lower()

    logger.info(f"Reading document: {file_path.name}")

    if extension == ".txt":
        return read_text_file(file_path)
    elif extension == ".pdf":
        return read_pdf_file(file_path)
    elif extension == ".doc":
        return read_doc_file(file_path)
    elif extension == ".docx":
        return read_docx_file(file_path)
    else:
        logger.warning(f"Unsupported file type: {extension}")
        return None


def get_file_size_mb(file_path: Path) -> float:
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)
