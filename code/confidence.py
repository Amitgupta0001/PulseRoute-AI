class ConfidenceEngine:

    @staticmethod
    def calculate(features):

        if not features or not isinstance(features, dict):
            return 0.50

        score = 0.50

        if features.get("verified_business"):
            score += 0.10

        if features.get("known_business"):
            score += 0.10

        if features.get("payment"):
            score += 0.08

        if features.get("urgent"):
            score += 0.06

        if features.get("event"):
            score += 0.05

        if features.get("promotion"):
            score -= 0.03

        if features.get("possible_scam"):
            score += 0.12

        if features.get("report_rate", 0) > 0.20:
            score += 0.10

        if features.get("reply_rate", 0) > 0.40:
            score += 0.05

        if features.get("dismiss_rate", 0) > 0.50:
            score += 0.05

        final_score = max(0.01, min(score, 0.99))

        return round(final_score, 2)