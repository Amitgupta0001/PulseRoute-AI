from dataclasses import dataclass
from typing import Optional


@dataclass
class IncomingMessage:

    message_id: str
    user_id: str

    conversation_type: str

    group_id: Optional[str]

    business_id: Optional[str]

    sender_user_id: Optional[str]

    created_at: str

    message_text: Optional[str]

    media_type: Optional[str]

    media_id: Optional[str]

    forwarded_count: int


@dataclass
class UserContext:

    user: dict

    group: Optional[dict]

    business: Optional[dict]

    history: list

    events: list

    notification_summary: list