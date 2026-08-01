from models import IncomingMessage, UserContext


class ContextRetriever:

    def __init__(self, loader):

        self.loader = loader

    def get_user(self, user_id):

        user = self.loader.users

        result = user[user["user_id"] == user_id]

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    def get_group(self, group_id):

        if group_id is None:
            return None

        groups = self.loader.groups

        result = groups[groups["group_id"] == group_id]

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    def get_group_membership(self, user_id, group_id):

        if group_id is None:
            return None

        df = self.loader.group_members

        result = df[
            (df["user_id"] == user_id)
            &
            (df["group_id"] == group_id)
        ]

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    def get_business(self, business_id):

        if business_id is None:
            return None

        df = self.loader.business_accounts

        result = df[df["business_id"] == business_id]

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    def get_business_history(self, user_id, business_id):

        if business_id is None:
            return None

        df = self.loader.user_business_history

        result = df[
            (df["user_id"] == user_id)
            &
            (df["business_id"] == business_id)
        ]

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    def get_message_history(self, user_id):

        df = self.loader.message_history

        history = df[df["user_id"] == user_id]

        return history.to_dict("records")

    def get_events(self, history):

        ids = [x["message_id"] for x in history]

        df = self.loader.message_events

        events = df[df["message_id"].isin(ids)]

        return events.to_dict("records")

    def get_notification_summary(self, user_id):

        df = self.loader.daily_notification_summary

        summary = df[df["user_id"] == user_id]

        return summary.to_dict("records")

    def retrieve(self, message: IncomingMessage):

        history = self.get_message_history(message.user_id)

        return UserContext(

            user=self.get_user(message.user_id),

            group=self.get_group(message.group_id),

            business=self.get_business(message.business_id),

            group_membership=self.get_group_membership(
                message.user_id,
                message.group_id
            ),

            business_history=self.get_business_history(
                message.user_id,
                message.business_id
            ),

            history=history,

            events=self.get_events(history),

            notification_summary=self.get_notification_summary(
                message.user_id
            )

        )