import pandas as pd
from config import OUTPUT_FILE, DATASET_DIR
from loader import DataLoader
from models import IncomingMessage
from context_retriever import ContextRetriever
from router import NotificationRouter
from evidence import EvidenceRetriever


def generate_predictions():
    loader = DataLoader().load()
    context_retriever = ContextRetriever(loader)
    router = NotificationRouter()
    evidence_engine = EvidenceRetriever()

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