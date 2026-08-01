from rapidfuzz import fuzz


class EvidenceRetriever:

    def __init__(self):
        pass

    def similarity(self, text1, text2):

        if not isinstance(text1, str):
            text1 = ""

        if not isinstance(text2, str):
            text2 = ""

        return fuzz.token_sort_ratio(text1, text2)

    def retrieve(self, message, context, top_k=3):

        history = context.history

        scored = []

        for old_message in history:

            score = self.similarity(
                message.message_text,
                old_message["message_text"]
            )

            if score > 40:
                scored.append(
                    (
                        score,
                        old_message["message_id"]
                    )
                )

        scored.sort(reverse=True)

        evidence = [
            message_id
            for _, message_id in scored[:top_k]
        ]

        if not evidence:
            return "none"

        return ";".join(evidence)