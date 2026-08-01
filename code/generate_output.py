import pandas as pd
from config import OUTPUT_FILE, DATASET_DIR
from loader import DataLoader
from models import IncomingMessage
from context_retriever import ContextRetriever
from router import NotificationRouter
from evidence import EvidenceRetriever
from media.ocr import OCREngine
from media.speech import SpeechEngine


def generate_predictions():
    loader = DataLoader().load()
    context_retriever = ContextRetriever(loader)
    router = NotificationRouter()
    evidence_engine = EvidenceRetriever()
    ocr_engine = OCREngine()
    speech_engine = SpeechEngine()

    images_map = {}
    if loader.images is not None and not loader.images.empty:
        for _, row in loader.images.iterrows():
            img_id = row.get("image_id")
            file_p = row.get("file_path")
            if img_id and file_p and pd.notna(img_id) and pd.notna(file_p):
                images_map[str(img_id)] = DATASET_DIR / str(file_p)

    voice_map = {}
    if loader.voice_notes is not None and not loader.voice_notes.empty:
        for _, row in loader.voice_notes.iterrows():
            vn_id = row.get("voice_note_id")
            file_p = row.get("file_path")
            if vn_id and file_p and pd.notna(vn_id) and pd.notna(file_p):
                voice_map[str(vn_id)] = DATASET_DIR / str(file_p)

    results = []

    for _, row in loader.messages.iterrows():
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
            if message.media_type == "image" or (message.media_id and str(message.media_id) in images_map):
                img_path = images_map.get(str(message.media_id))
                if img_path and img_path.is_file():
                    extracted_text = ocr_engine.extract_text(str(img_path))
                    if extracted_text:
                        message.message_text = extracted_text
            elif message.media_type == "voice" or (message.media_id and str(message.media_id) in voice_map):
                audio_path = voice_map.get(str(message.media_id))
                if audio_path and audio_path.is_file():
                    transcript = speech_engine.transcribe(str(audio_path))
                    if transcript:
                        message.message_text = transcript

        context = context_retriever.retrieve(message)
        decision = router.route(message, context)
        evidence = evidence_engine.retrieve(message, context)

        results.append({
            "message_id": message.message_id,
            "action": decision["action"],
            "message_type": decision["message_type"],
            "reason": decision["reason"],
            "confidence": decision["confidence"],
            "evidence_message_ids": evidence,
        })

    df = pd.DataFrame(results)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    dataset_output = DATASET_DIR / "output.csv"
    df.to_csv(dataset_output, index=False)

    root_output = OUTPUT_FILE.parent.parent.parent / "output.csv"
    df.to_csv(root_output, index=False)

    print(f"Generated predictions for {len(df)} messages.")
    print(f"Saved output to:\n  - {OUTPUT_FILE}\n  - {dataset_output}\n  - {root_output}")

    return df


def main():
    generate_predictions()


if __name__ == "__main__":
    main()