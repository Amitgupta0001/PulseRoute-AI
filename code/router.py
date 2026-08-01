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

        # =====================================================
        # 1. SCAM DETECTION
        # =====================================================

        if (
            features["possible_scam"]
            or features["report_rate"] >= 0.20
            or message.forwarded_count >= 10
        ):
            return {
                "action": "mute",
                "message_type": "scam",
                "reason": "Suspicious or scam-like message detected.",
                "confidence": confidence,
            }

        # =====================================================
        # 2. VERIFIED BANK PAYMENTS
        # =====================================================

        if business is not None:

            if (
                business["category"] == "bank"
                and business["verified"] == 1
                and features["payment"]
            ):

                return {
                    "action": "notify",
                    "message_type": "payment",
                    "reason": "Trusted banking payment update.",
                    "confidence": confidence,
                }

        # =====================================================
        # 3. PROMOTIONS
        # =====================================================

        if features["promotion"]:

            if (
                business_history is not None
                and business_history["allows_promotions"] == 1
            ):

                return {
                    "action": "digest",
                    "message_type": "promotion",
                    "reason": "User is subscribed to promotional messages.",
                    "confidence": confidence,
                }

            return {
                "action": "mute",
                "message_type": "promotion",
                "reason": "Promotional content not relevant to this user.",
                "confidence": confidence,
            }

        # =====================================================
        # 4. FAMILY GROUP
        # =====================================================

        if group is not None:

            if group["group_type"] == "family":

                return {
                    "action": "notify",
                    "message_type": "personal",
                    "reason": "Family conversations are prioritized.",
                    "confidence": confidence,
                }

        # =====================================================
        # 5. SCHOOL GROUP
        # =====================================================

        if group is not None:

            if (
                group["group_type"] == "school"
                and features["event"]
            ):

                return {
                    "action": "notify",
                    "message_type": "event",
                    "reason": "Important school announcement.",
                    "confidence": confidence,
                }

        # =====================================================
        # 6. WORK GROUP
        # =====================================================

        if group is not None:

            if group["group_type"] == "work":

                if (
                    membership is not None
                    and membership["replies_sent_30d"] >= 5
                ):

                    return {
                        "action": "notify",
                        "message_type": "personal",
                        "reason": "Active work discussion.",
                        "confidence": confidence,
                    }

                return {
                    "action": "digest",
                    "message_type": "personal",
                    "reason": "Work-related discussion.",
                    "confidence": confidence,
                }

        # =====================================================
        # 7. MUTED GROUP
        # =====================================================

        if (
            membership is not None
            and membership["group_muted_by_user"] == 1
        ):

            return {
                "action": "mute",
                "message_type": "unknown",
                "reason": "This group is muted by the user.",
                "confidence": confidence,
            }

        # =====================================================
        # 8. DO NOT DISTURB
        # =====================================================

        if features["dnd"]:

            if (
                not features["urgent"]
                and not features["payment"]
            ):

                return {
                    "action": "digest",
                    "message_type": "unknown",
                    "reason": "Delivered during do-not-disturb hours.",
                    "confidence": confidence,
                }

        # =====================================================
        # 9. USER HISTORY
        # =====================================================

        if features["reply_rate"] >= 0.40:

            return {
                "action": "notify",
                "message_type": "personal",
                "reason": "User usually responds to similar messages.",
                "confidence": confidence,
            }

        if features["dismiss_rate"] >= 0.50:

            return {
                "action": "mute",
                "message_type": "unknown",
                "reason": "User frequently dismisses similar notifications.",
                "confidence": confidence,
            }

        # =====================================================
        # 10. URGENT PERSONAL MESSAGE
        # =====================================================

        if (
            message.conversation_type == "personal"
            and features["urgent"]
        ):

            return {
                "action": "notify",
                "message_type": "urgent",
                "reason": "Urgent personal message.",
                "confidence": confidence,
            }

        # =====================================================
        # DEFAULT
        # =====================================================

        return {
            "action": "digest",
            "message_type": "unknown",
            "reason": "Useful but not immediately important.",
            "confidence": confidence,
        }