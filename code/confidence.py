class ConfidenceEngine:

    @staticmethod
    def calculate(features):

        score = 0.50

        if features["verified_business"]:
            score += 0.10

        if features["known_business"]:
            score += 0.10

        if features["payment"]:
            score += 0.08

        if features["urgent"]:
            score += 0.06

        if features["event"]:
            score += 0.05

        if features["promotion"]:
            score -= 0.03

        if features["possible_scam"]:
            score += 0.12

        if features["report_rate"] > 0.20:
            score += 0.10

        if features["reply_rate"] > 0.40:
            score += 0.05

        if features["dismiss_rate"] > 0.50:
            score += 0.05

        return round(min(score, 0.99), 2)