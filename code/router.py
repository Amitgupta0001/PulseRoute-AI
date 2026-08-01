from feature_engine import FeatureEngine


class NotificationRouter:

    def route(self, message, context):

        features = FeatureEngine.build(message, context)

        # ----------------------------
        # 1. Scam Detection
        # ----------------------------
        if (
            features["possible_scam"]
            or features["report_rate"] > 0.20
            or features["forwarded"] >= 10
        ):
            return {
                "action": "mute",
                "message_type": "scam",
                "reason": "Possible scam or unsafe content.",
                "confidence": 0.96,
            }

        # ----------------------------
        # 2. Trusted Payment Messages
        # ----------------------------
        if (
            features["payment"]
            and features["verified_business"]
            and features["known_business"]
        ):
            return {
                "action": "notify",
                "message_type": "payment",
                "reason": "Trusted payment update from a known business.",
                "confidence": 0.95,
            }

        # ----------------------------
        # 3. Promotion
        # ----------------------------
        if features["promotion"]:

            if features["promotion_allowed"]:

                return {
                    "action": "digest",
                    "message_type": "promotion",
                    "reason": "Promotional message from an opted-in business.",
                    "confidence": 0.84,
                }

            return {
                "action": "mute",
                "message_type": "promotion",
                "reason": "Promotional message not relevant to this user.",
                "confidence": 0.88,
            }

        # ----------------------------
        # 4. Events
        # ----------------------------
        if features["event"]:

            return {
                "action": "notify",
                "message_type": "event",
                "reason": "Upcoming event may require attention.",
                "confidence": 0.86,
            }

        # ----------------------------
        # 5. Urgent Personal
        # ----------------------------
        if (
            message.conversation_type == "personal"
            and features["urgent"]
        ):

            return {
                "action": "notify",
                "message_type": "urgent",
                "reason": "Urgent personal communication.",
                "confidence": 0.90,
            }

        # ----------------------------
        # 6. Group Behaviour
        # ----------------------------
        membership = context.group_membership

        if membership is not None:

            if membership["group_muted_by_user"] == 1:

                return {
                    "action": "mute",
                    "message_type": "unknown",
                    "reason": "User has muted this group.",
                    "confidence": 0.93,
                }

            if membership["replies_sent_30d"] > 5:

                return {
                    "action": "notify",
                    "message_type": "personal",
                    "reason": "User actively participates in this group.",
                    "confidence": 0.82,
                }

        # ----------------------------
        # 7. Historical Behaviour
        # ----------------------------
        if features["reply_rate"] > 0.40:

            return {
                "action": "notify",
                "message_type": "personal",
                "reason": "User frequently responds to similar messages.",
                "confidence": 0.81,
            }

        if features["dismiss_rate"] > 0.50:

            return {
                "action": "mute",
                "message_type": "unknown",
                "reason": "Similar messages are usually ignored.",
                "confidence": 0.84,
            }

        # ----------------------------
        # Default
        # ----------------------------
        return {
            "action": "digest",
            "message_type": "unknown",
            "reason": "Useful but not urgent.",
            "confidence": 0.72,
        }