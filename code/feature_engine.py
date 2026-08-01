import re
from datetime import datetime
import pandas as pd

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
    "wallet kyc",
    "login code"
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


def _safe_int(val):
    if val is None or pd.isna(val):
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0


class FeatureEngine:

    @staticmethod
    def contains(text, keywords):

        if not isinstance(text, str) or not text:
            return False

        text_lower = text.lower()

        for kw in keywords:
            kw_lower = kw.lower()
            if " " in kw_lower:
                if kw_lower in text_lower:
                    return True
            else:
                pattern = r'\b' + re.escape(kw_lower) + r'\b'
                if re.search(pattern, text_lower):
                    return True

        return False

    @staticmethod
    def build(message, context):

        text = message.message_text or ""

        history = context.history if context and context.history else []
        events = context.events if context and context.events else []

        opened = sum(_safe_int(e.get("message_opened")) for e in events)
        replied = sum(_safe_int(e.get("message_replied")) for e in events)
        dismissed = sum(_safe_int(e.get("notification_dismissed")) for e in events)
        reported = sum(_safe_int(e.get("message_reported")) for e in events)

        known_biz = context.business_history is not None if context else False
        promo_allowed = False
        if context and context.business_history:
            val = context.business_history.get("allows_promotions")
            promo_allowed = bool(val == 1 or val is True)

        verified_biz = False
        if context and context.business:
            val = context.business.get("verified")
            verified_biz = bool(val == 1 or val is True)

        hist_count = len(history)

        return {

            "verified_business": verified_biz,

            "known_business": known_biz,

            "promotion_allowed": promo_allowed,

            "forwarded": message.forwarded_count if message else 0,

            "payment": FeatureEngine.contains(text, PAYMENT_KEYWORDS),

            "urgent": FeatureEngine.contains(text, URGENT_KEYWORDS),

            "promotion": FeatureEngine.contains(text, PROMOTION_KEYWORDS),

            "event": FeatureEngine.contains(text, EVENT_KEYWORDS),

            "possible_scam": FeatureEngine.contains(text, SCAM_KEYWORDS),

            "dnd": FeatureEngine.is_in_dnd_window(message, context),

            "history_messages": hist_count,

            "opened": opened,

            "replied": replied,

            "dismissed": dismissed,

            "reported": reported,

            "reply_rate": replied / max(1, hist_count),

            "open_rate": opened / max(1, hist_count),

            "dismiss_rate": dismissed / max(1, hist_count),

            "report_rate": reported / max(1, hist_count)
        }

    @staticmethod
    def is_in_dnd_window(message, context):

        if not context or not context.user or not message or not message.created_at:
            return False

        user = context.user
        window = user.get("do_not_disturb_window")

        if not isinstance(window, str) or "-" not in window:
            return False

        try:
            parts = window.split("-")
            if len(parts) != 2:
                return False

            start_str, end_str = parts[0].strip(), parts[1].strip()

            created_str = str(message.created_at).strip()
            msg_time = None
            for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%H:%M"):
                try:
                    msg_time = datetime.strptime(created_str, fmt).time()
                    break
                except ValueError:
                    continue

            if msg_time is None:
                return False

            start = datetime.strptime(start_str, "%H:%M").time()
            end = datetime.strptime(end_str, "%H:%M").time()

            if start < end:
                return start <= msg_time <= end

            return msg_time >= start or msg_time <= end
        except Exception:
            return False