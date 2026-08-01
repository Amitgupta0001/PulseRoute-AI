import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SpeechEngine:

    def __init__(
        self,
        model_size: str = "tiny",
        device: str = "cpu",
        compute_type: str = "int8"
    ):

        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self._initialized = False

    def _init_model(self):

        if not self._initialized:
            try:
                # pyrefly: ignore [missing-import]
                from faster_whisper import WhisperModel
                self.model = WhisperModel(
                    self.model_size,
                    device=self.device,
                    compute_type=self.compute_type
                )
            except Exception as e:
                logger.warning(f"Faster-Whisper initialization failed: {e}")
                self.model = None
            self._initialized = True

    def transcribe(self, audio_path: str) -> str:

        if not audio_path:
            return ""

        path = Path(audio_path)

        if not path.is_file():
            return ""

        self._init_model()

        if self.model is None:
            return ""

        try:
            segments, _ = self.model.transcribe(str(path), beam_size=1)
            transcription = " ".join([segment.text for segment in segments]).strip()
            return transcription
        except Exception as e:
            logger.error(f"Speech transcription failed for {audio_path}: {e}")

        return ""
