from hackathon.code import confidence
from feature_engine import FeatureEngine
from confidence import ConfidenceEngine


class NotificationRouter:

    def route(self, message, context):

        features = FeatureEngine.build(message, context)
        confidence = ConfidenceEngine.calculate(features)

        group = context.group
        membership = context.group_membership
        business = context.business
        business_history = context.business_history

        # -------------------------------------------------
        # SCAM
        # -------------------------------------------------

        if (
            features["possible_scam"]
            or features["report_rate"] > 0.20
            or message.forwarded_count >= 10
        ):
            return {
                "action": "mute",
                "message_type": "scam",
                "reason": "Potential scam or suspicious content.",
                "confidence": confidence,
            }

        # -------------------------------------------------
        # VERIFIED BANK
        # -------------------------------------------------

        if business:

            category = business["category"]

            if (
                category == "bank"
                and business["verified"] == 1
                and features["payment"]
            ):

                return {
                    "action": "notify",
                    "message_type": "payment",
                    "reason": "Trusted banking update requiring attention.",
                    "confidence": confidence,
                }

        # -------------------------------------------------
        # PROMOTIONS
        # -------------------------------------------------

        if business_history:

            if (
                features["promotion"]
                and business_history["allows_promotions"] == 0
            ):

                return {
                    "action": "mute",
                    "message_type": "promotion",
                    "reason": "User has not opted in to promotions.",
                    "confidence": confidence,
                }

        # -------------------------------------------------
        # FAMILY GROUP
        # -------------------------------------------------

        if group:

            if group["group_type"] == "family":

                return {
                    "action": "notify",
                    "message_type": "personal",
                    "reason": "Family messages are prioritized.",
                    "confidence": confidence,
                }

        # -------------------------------------------------
        # SCHOOL GROUP
        # -------------------------------------------------

        if group:

            if (
                group["group_type"] == "school"
                and features["event"]
            ):

                return {
                    "action": "notify",
                    "message_type": "event",
                    "reason": "Important school update.",
                    "confidence": confidence,
                }

        # -------------------------------------------------
        # WORK GROUP
        # -------------------------------------------------

        if group:

            if group["group_type"] == "work":

                if membership:

                    if membership["replies_sent_30d"] >= 5:

                        return {
                            "action": "notify",
                            "message_type": "personal",
                            "reason": "Active work conversation.",
                            "confidence": confidence,
                        }

                return {
                    "action": "digest",
                    "message_type": "personal",
                    "reason": "Work-related discussion.",
                    "confidence": confidence,
                }

        # -------------------------------------------------
        # MUTED GROUP
        # -------------------------------------------------

        if membership:

            if membership["group_muted_by_user"] == 1:

                return {
                    "action": "mute",
                    "message_type": "unknown",
                    "reason": "User muted this group.",
                    "confidence": confidence,
                }

        # -------------------------------------------------
        # HISTORY
        # -------------------------------------------------

        if features["reply_rate"] > 0.50:

            return {
                "action": "notify",
                "message_type": "personal",
                "reason": "User frequently replies to similar messages.",
                "confidence": confidence,
            }

        if features["dismiss_rate"] > 0.50:

            return {
                "action": "mute",
                "message_type": "unknown",
                "reason": "User usually ignores similar messages.",
                "confidence": confidence,
            }
        # ----------------------------------------
        # DO NOT DISTURB
        # ----------------------------------------
        if features["dnd"]:
            if (
                not features["urgent"]
                and not features["payment"]
            ):
                return {
                    "action": "digest",
                    "message_type": "unknown",
                    "reason": "Delivered during user's do-not-disturb window.",
                    "confidence": confidence
                }

        # -------------------------------------------------
        # DEFAULT
        # -------------------------------------------------

        return {
            "action": "digest",
            "message_type": "unknown",
            "reason": "Useful but not immediately important.",
            "confidence": confidence,
        }