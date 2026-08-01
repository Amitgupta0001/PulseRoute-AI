from feature_engine import FeatureEngine
from confidence import ConfidenceEngine




class NotificationRouter:

    def route(self, message, context):

        features = FeatureEngine.build(message, context)
        confidence = ConfidenceEngine.calculate(features)

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
                "confidence": confidence,
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
                "confidence": confidence,
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
                    "confidence": confidence,
                }

            return {
                "action": "mute",
                "message_type": "promotion",
                "reason": "Promotional message not relevant to this user.",
                "confidence": confidence,
            }

        # ----------------------------
        # 4. Events
        # ----------------------------
        if features["event"]:

            return {
                "action": "notify",
                "message_type": "event",
                "reason": "Upcoming event may require attention.",
                "confidence": confidence,
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
                "confidence": confidence,
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
                    "confidence": confidence,
                }

            if membership["replies_sent_30d"] > 5:

                return {
                    "action": "notify",
                    "message_type": "personal",
                    "reason": "User actively participates in this group.",
                    "confidence": confidence,
                }

        # ----------------------------
        # 7. Historical Behaviour
        # ----------------------------
        if features["reply_rate"] > 0.40:

            return {
                "action": "notify",
                "message_type": "personal",
                "reason": "User frequently responds to similar messages.",
                "confidence": confidence,
            }

        if features["dismiss_rate"] > 0.50:

            return {
                "action": "mute",
                "message_type": "unknown",
                "reason": "Similar messages are usually ignored.",
                "confidence": confidence,
            }

        # ----------------------------
        # Default
        # ----------------------------
        return {
            "action": "digest",
            "message_type": "unknown",
            "reason": "Useful but not urgent.",
            "confidence": confidence,
        }