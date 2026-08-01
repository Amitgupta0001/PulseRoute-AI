import pandas as pd

from data_loader import DataLoader
from domain_models import IncomingMessage
from context_retriever import ContextRetriever
from router import NotificationRouter
from evidence import EvidenceRetriever
from app_config import OUTPUT_FILE


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

        forwarded_count=row["forwarded_count"]
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

        "evidence_message_ids": evidence
    })


df = pd.DataFrame(results)

df.to_csv(OUTPUT_FILE, index=False)

print(df.head())

print()

print("Saved to")

print(OUTPUT_FILE)