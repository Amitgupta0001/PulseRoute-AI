import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class OCREngine:

    def __init__(self, use_gpu: bool = False):

        self.reader = None
        self._initialized = False
        self.use_gpu = use_gpu

    def _init_reader(self):

        if not self._initialized:
            try:
                import easyocr
                self.reader = easyocr.Reader(["en"], gpu=self.use_gpu)
            except Exception as e:
                logger.warning(f"EasyOCR initialization failed: {e}")
                self.reader = None
            self._initialized = True

    def extract_text(self, image_path: str) -> str:

        if not image_path:
            return ""

        path = Path(image_path)

        if not path.is_file():
            return ""

        self._init_reader()

        if self.reader is None:
            return ""

        try:
            results = self.reader.readtext(str(path), detail=0)
            if results:
                return " ".join(results).strip()
        except Exception as e:
            logger.error(f"OCR extraction failed for {image_path}: {e}")

        return ""
