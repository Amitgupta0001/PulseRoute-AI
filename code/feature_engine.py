import re
from datetime import datetime

PAYMENT_KEYWORDS = {
    "bill",
    "payment",
    "due",
    "invoice",
    "credit",
    "debit",
    "statement",
    "bank",
    "upi",
    "emi",
    "transaction",
    "refund"
}

URGENT_KEYWORDS = {
    "urgent",
    "immediately",
    "asap",
    "today",
    "deadline",
    "important",
    "alert"
}

PROMOTION_KEYWORDS = {
    "offer",
    "sale",
    "discount",
    "coupon",
    "cashback",
    "deal",
    "voucher",
    "buy",
    "free"
}

SCAM_KEYWORDS = {
    "otp",
    "pin",
    "verify",
    "claim prize",
    "lottery",
    "crypto",
    "investment",
    "click here",
    "payment link",
    "wallet kyc"
}

EVENT_KEYWORDS = {
    "meeting",
    "event",
    "ceremony",
    "birthday",
    "wedding",
    "exam",
    "class",
    "schedule"
}


class FeatureEngine:

    @staticmethod
    def contains(text, keywords):

        if not isinstance(text, str):
            return False

        text = text.lower()

        return any(word in text for word in keywords)

    @staticmethod
    def build(message, context):

        text = message.message_text or ""

        history = context.history
        events = context.events

        opened = sum(e["message_opened"] for e in events)
        replied = sum(e["message_replied"] for e in events)
        dismissed = sum(e["notification_dismissed"] for e in events)
        reported = sum(e["message_reported"] for e in events)

        return {

            "verified_business":
            bool(context.business and context.business["verified"]),

            "known_business":
            context.business_history is not None,

            "promotion_allowed":
            bool(
                context.business_history
                and context.business_history["allows_promotions"]
            ),

            "forwarded":
            message.forwarded_count,

            "payment":
            FeatureEngine.contains(text, PAYMENT_KEYWORDS),

            "urgent":
            FeatureEngine.contains(text, URGENT_KEYWORDS),

            "promotion":
            FeatureEngine.contains(text, PROMOTION_KEYWORDS),

            "event":
            FeatureEngine.contains(text, EVENT_KEYWORDS),

            "possible_scam":
            FeatureEngine.contains(text, SCAM_KEYWORDS),

            "history_messages":
            len(history),

            "opened":
            opened,

            "replied":
            replied,

            "dismissed":
            dismissed,

            "reported":
            reported,

            "reply_rate":
            replied / max(1, len(history)),

            "open_rate":
            opened / max(1, len(history)),

            "dismiss_rate":
            dismissed / max(1, len(history)),

            "report_rate":
            reported / max(1, len(history))
        }

    @staticmethod
    def is_in_dnd_window(message, context):

        user = context.user

        if user is None:
            return False

        window = user["do_not_disturb_window"]

        if not isinstance(window, str):
            return False

        start, end = window.split("-")

        msg_time = datetime.strptime(
            message.created_at,
            "%Y-%m-%d %H:%M"
        ).time()

        start = datetime.strptime(start, "%H:%M").time()
        end = datetime.strptime(end, "%H:%M").time()

        if start < end:
            return start <= msg_time <= end

        return msg_time >= start or msg_time <= end