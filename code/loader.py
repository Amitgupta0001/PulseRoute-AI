import pandas as pd

from config import DATASET_DIR


class DataLoader:

    def __init__(self):

        self.messages = None
        self.users = None
        self.groups = None
        self.group_members = None
        self.business_accounts = None
        self.user_business_history = None
        self.message_history = None
        self.message_events = None
        self.images = None
        self.voice_notes = None
        self.daily_notification_summary = None
        self.sample_messages = None

    def load(self):

        self.messages = pd.read_csv(DATASET_DIR / "messages.csv")

        self.users = pd.read_csv(DATASET_DIR / "users.csv")

        self.groups = pd.read_csv(DATASET_DIR / "groups.csv")

        self.group_members = pd.read_csv(DATASET_DIR / "group_members.csv")

        self.business_accounts = pd.read_csv(
            DATASET_DIR / "business_accounts.csv"
        )

        self.user_business_history = pd.read_csv(
            DATASET_DIR / "user_business_history.csv"
        )

        self.message_history = pd.read_csv(
            DATASET_DIR / "message_history.csv"
        )

        self.message_events = pd.read_csv(
            DATASET_DIR / "message_events.csv"
        )

        self.images = pd.read_csv(DATASET_DIR / "images.csv")

        self.voice_notes = pd.read_csv(DATASET_DIR / "voice_notes.csv")

        self.daily_notification_summary = pd.read_csv(
            DATASET_DIR / "daily_notification_summary.csv"
        )

        self.sample_messages = pd.read_csv(
            DATASET_DIR / "sample_messages.csv"
        )

        return self