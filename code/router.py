from feature_engine import FeatureEngine
from confidence import ConfidenceEngine


class NotificationRouter:

    def route(self, message, context):

        features = FeatureEngine.build(message, context)
        confidence = ConfidenceEngine.calculate(features)

        group = context.group if context else None
        membership = context.group_membership if context else None
        business = context.business if context else None
        business_history = context.business_history if context else None

        # =====================================================
        # 1. SCAM DETECTION
        # =====================================================

        forwarded = message.forwarded_count if message else 0

        if (
            features.get("possible_scam")
            or features.get("report_rate", 0) >= 0.20
            or forwarded >= 10
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

            cat = business.get("category")
            ver = business.get("verified")

            if (
                cat == "bank"
                and (ver == 1 or ver is True)
                and features.get("payment")
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

        if features.get("promotion"):

            if business_history is not None:

                allows = business_history.get("allows_promotions")

                if allows == 1 or allows is True:

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

            if group.get("group_type") == "family":

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
                group.get("group_type") == "school"
                and features.get("event")
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

            if group.get("group_type") == "work":

                replies = membership.get("replies_sent_30d", 0) if membership else 0

                if replies >= 5:

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

        if membership is not None:

            muted = membership.get("group_muted_by_user")

            if muted == 1 or muted is True:

                return {
                    "action": "mute",
                    "message_type": "unknown",
                    "reason": "This group is muted by the user.",
                    "confidence": confidence,
                }

        # =====================================================
        # 8. DO NOT DISTURB
        # =====================================================

        if features.get("dnd"):

            if (
                not features.get("urgent")
                and not features.get("payment")
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

        if features.get("reply_rate", 0) >= 0.40:

            return {
                "action": "notify",
                "message_type": "personal",
                "reason": "User usually responds to similar messages.",
                "confidence": confidence,
            }

        if features.get("dismiss_rate", 0) >= 0.50:

            return {
                "action": "mute",
                "message_type": "unknown",
                "reason": "User frequently dismisses similar notifications.",
                "confidence": confidence,
            }

        # =====================================================
        # 10. URGENT PERSONAL MESSAGE
        # =====================================================

        if message and message.conversation_type == "personal":

            if features.get("urgent"):

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