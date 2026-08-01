import pandas as pd
from models import IncomingMessage, UserContext


class ContextRetriever:

    def __init__(self, loader):

        self.loader = loader
        self._build_cache()

    def _build_cache(self):

        self._users = {}
        if self.loader.users is not None and not self.loader.users.empty:
            for row in self.loader.users.to_dict("records"):
                uid = row.get("user_id")
                if uid and pd.notna(uid):
                    self._users[str(uid)] = row

        self._groups = {}
        if self.loader.groups is not None and not self.loader.groups.empty:
            for row in self.loader.groups.to_dict("records"):
                gid = row.get("group_id")
                if gid and pd.notna(gid):
                    self._groups[str(gid)] = row

        self._group_members = {}
        if self.loader.group_members is not None and not self.loader.group_members.empty:
            for row in self.loader.group_members.to_dict("records"):
                uid = row.get("user_id")
                gid = row.get("group_id")
                if uid and gid and pd.notna(uid) and pd.notna(gid):
                    self._group_members[(str(uid), str(gid))] = row

        self._business = {}
        if self.loader.business_accounts is not None and not self.loader.business_accounts.empty:
            for row in self.loader.business_accounts.to_dict("records"):
                bid = row.get("business_id")
                if bid and pd.notna(bid):
                    self._business[str(bid)] = row

        self._business_history = {}
        if self.loader.user_business_history is not None and not self.loader.user_business_history.empty:
            for row in self.loader.user_business_history.to_dict("records"):
                uid = row.get("user_id")
                bid = row.get("business_id")
                if uid and bid and pd.notna(uid) and pd.notna(bid):
                    self._business_history[(str(uid), str(bid))] = row

        self._message_history = {}
        if self.loader.message_history is not None and not self.loader.message_history.empty:
            for row in self.loader.message_history.to_dict("records"):
                uid = row.get("user_id")
                if uid and pd.notna(uid):
                    uid_str = str(uid)
                    if uid_str not in self._message_history:
                        self._message_history[uid_str] = []
                    self._message_history[uid_str].append(row)

        self._message_events = {}
        if self.loader.message_events is not None and not self.loader.message_events.empty:
            for row in self.loader.message_events.to_dict("records"):
                mid = row.get("message_id")
                if mid and pd.notna(mid):
                    mid_str = str(mid)
                    if mid_str not in self._message_events:
                        self._message_events[mid_str] = []
                    self._message_events[mid_str].append(row)

        self._daily_summary = {}
        if self.loader.daily_notification_summary is not None and not self.loader.daily_notification_summary.empty:
            for row in self.loader.daily_notification_summary.to_dict("records"):
                uid = row.get("user_id")
                if uid and pd.notna(uid):
                    uid_str = str(uid)
                    if uid_str not in self._daily_summary:
                        self._daily_summary[uid_str] = []
                    self._daily_summary[uid_str].append(row)

    def get_user(self, user_id):

        if not user_id or pd.isna(user_id):
            return None

        return self._users.get(str(user_id))

    def get_group(self, group_id):

        if not group_id or pd.isna(group_id):
            return None

        return self._groups.get(str(group_id))

    def get_group_membership(self, user_id, group_id):

        if not user_id or pd.isna(user_id) or not group_id or pd.isna(group_id):
            return None

        return self._group_members.get((str(user_id), str(group_id)))

    def get_business(self, business_id):

        if not business_id or pd.isna(business_id):
            return None

        return self._business.get(str(business_id))

    def get_business_history(self, user_id, business_id):

        if not user_id or pd.isna(user_id) or not business_id or pd.isna(business_id):
            return None

        return self._business_history.get((str(user_id), str(business_id)))

    def get_message_history(self, user_id):

        if not user_id or pd.isna(user_id):
            return []

        return self._message_history.get(str(user_id), [])

    def get_events(self, history):

        if not history:
            return []

        events = []
        for item in history:
            mid = item.get("message_id")
            if mid and pd.notna(mid):
                events.extend(self._message_events.get(str(mid), []))

        return events

    def get_notification_summary(self, user_id):

        if not user_id or pd.isna(user_id):
            return []

        return self._daily_summary.get(str(user_id), [])

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