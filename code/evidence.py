from rapidfuzz import fuzz
import pandas as pd


class EvidenceRetriever:

    def __init__(self):
        pass

    def similarity(self, text1, text2):

        if not isinstance(text1, str) or pd.isna(text1):
            text1 = ""

        if not isinstance(text2, str) or pd.isna(text2):
            text2 = ""

        text1 = text1.strip()
        text2 = text2.strip()

        if not text1 or not text2:
            return 0.0

        return float(fuzz.token_sort_ratio(text1, text2))

    def retrieve(self, message, context, top_k=3):

        if not context or not context.history:
            return "none"

        history = context.history
        scored = []
        msg_text = message.message_text if message and isinstance(message.message_text, str) else ""
        conv_type = message.conversation_type if message else None

        for old_message in history:
            old_id = old_message.get("message_id")
            if not old_id or pd.isna(old_id):
                continue

            old_text = old_message.get("message_text")
            if not isinstance(old_text, str) or pd.isna(old_text):
                old_text = ""

            text_sim = self.similarity(msg_text, old_text)

            meta_score = 0.0
            if message.sender_user_id and old_message.get("sender_user_id") == message.sender_user_id:
                meta_score += 45.0
            if message.business_id and old_message.get("business_id") == message.business_id:
                meta_score += 35.0
            if message.media_type and old_message.get("media_type") == message.media_type:
                meta_score += 25.0
            if message.group_id and old_message.get("group_id") == message.group_id:
                meta_score += 20.0
            if conv_type and old_message.get("conversation_type") == conv_type:
                meta_score += 15.0

            total_score = (text_sim * 0.6 + meta_score * 0.4) if text_sim > 0 else meta_score

            if total_score > 40.0:
                scored.append((total_score, str(old_id)))

        scored.sort(key=lambda x: x[0], reverse=True)

        evidence = []
        seen = set()

        for _, message_id in scored:
            if message_id not in seen:
                seen.add(message_id)
                evidence.append(message_id)
                if len(evidence) == top_k:
                    break

        if not evidence:
            return "none"

        return ";".join(evidence)