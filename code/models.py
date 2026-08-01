from dataclasses import dataclass
from typing import Optional
import pandas as pd


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

    forwarded_count: int = 0

    def __post_init__(self):
        if pd.isna(self.group_id) or not isinstance(self.group_id, str):
            self.group_id = None
        if pd.isna(self.business_id) or not isinstance(self.business_id, str):
            self.business_id = None
        if pd.isna(self.sender_user_id) or not isinstance(self.sender_user_id, str):
            self.sender_user_id = None
        if pd.isna(self.message_text) or not isinstance(self.message_text, str):
            self.message_text = None
        if pd.isna(self.media_type) or not isinstance(self.media_type, str):
            self.media_type = None
        if pd.isna(self.media_id) or not isinstance(self.media_id, str):
            self.media_id = None

        try:
            if pd.isna(self.forwarded_count):
                self.forwarded_count = 0
            else:
                self.forwarded_count = int(self.forwarded_count)
        except (ValueError, TypeError):
            self.forwarded_count = 0


@dataclass
class UserContext:

    user: dict

    group: Optional[dict]

    business: Optional[dict]

    group_membership: Optional[dict]

    business_history: Optional[dict]

    history: list

    events: list

    notification_summary: list