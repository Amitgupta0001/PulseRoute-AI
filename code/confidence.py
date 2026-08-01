class ConfidenceEngine:

    @staticmethod
    def calculate(features):

        if not features or not isinstance(features, dict):
            return 0.84

        score = 0.75

        if features.get("verified_business"):
            score += 0.04

        if features.get("known_business"):
            score += 0.03

        if features.get("payment"):
            score += 0.03

        if features.get("urgent"):
            score += 0.03

        if features.get("event"):
            score += 0.02

        if features.get("possible_scam"):
            score += 0.05

        if features.get("report_rate", 0) >= 0.20:
            score += 0.04

        if features.get("reply_rate", 0) >= 0.40:
            score += 0.03

        if features.get("dismiss_rate", 0) >= 0.50:
            score += 0.03

        if features.get("promotion") and not features.get("promotion_allowed"):
            score += 0.02

        if features.get("dnd") and not features.get("urgent") and not features.get("payment"):
            score -= 0.02

        final_score = max(0.70, min(score, 0.95))

        return round(final_score, 2)