from loader import DataLoader
from context_retriever import ContextRetriever
from models import IncomingMessage
from feature_engine import FeatureEngine
from router import NotificationRouter

loader = DataLoader().load()

retriever = ContextRetriever(loader)

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

context = retriever.retrieve(message)
features = FeatureEngine.build(message, context)
router = NotificationRouter()
decision = router.route(message, context)

print()

print("=" * 60)

print(decision)

for key, value in features.items():
    print(f"{key:25} : {value}")

print(context)