import pandas as pd
from config import DATASET_DIR
from loader import DataLoader
from context_retriever import ContextRetriever
from models import IncomingMessage
from feature_engine import FeatureEngine
from router import NotificationRouter
from evidence import EvidenceRetriever
from media.ocr import OCREngine
from media.speech import SpeechEngine
from generate_output import generate_predictions

loader = DataLoader().load()
retriever = ContextRetriever(loader)
ocr_engine = OCREngine()
speech_engine = SpeechEngine()

row = loader.messages.iloc[0]

message = IncomingMessage(
    message_id=row["message_id"],
    user_id=row["user_id"],
    conversation_type=row["conversation_type"],
    group_id=row["group_id"],
    business_id=row["business_id"],
    sender_user_id=row["sender_user_id"],
    created_at=row["created_at"],
    message_text=row["message_text"],
    media_type=row["media_type"],
    media_id=row["media_id"],
    forwarded_count=row["forwarded_count"],
)

if not message.message_text or pd.isna(message.message_text):
    if message.media_type == "image":
        if loader.images is not None and not loader.images.empty:
            match = loader.images[loader.images["image_id"] == message.media_id]
            if not match.empty:
                img_path = DATASET_DIR / str(match.iloc[0]["file_path"])
                if img_path.is_file():
                    extracted = ocr_engine.extract_text(str(img_path))
                    if extracted:
                        message.message_text = extracted
    elif message.media_type == "voice":
        if loader.voice_notes is not None and not loader.voice_notes.empty:
            match = loader.voice_notes[loader.voice_notes["voice_note_id"] == message.media_id]
            if not match.empty:
                audio_path = DATASET_DIR / str(match.iloc[0]["file_path"])
                if audio_path.is_file():
                    transcript = speech_engine.transcribe(str(audio_path))
                    if transcript:
                        message.message_text = transcript

context = retriever.retrieve(message)
features = FeatureEngine.build(message, context)
router = NotificationRouter()
decision = router.route(message, context)
evidence_retriever = EvidenceRetriever()
evidence = evidence_retriever.retrieve(message, context)

print("Sample Message Evidence:", evidence)
print()
print("=" * 60)
print("Sample Message Decision:", decision)
print("Features:")
for key, value in features.items():
    print(f"{key:25} : {value}")

print("\nGenerating output predictions for all messages...")
generate_predictions()