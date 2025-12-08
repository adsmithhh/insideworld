
class PresenceOverlayOrchestrator:
    def __init__(self, overlay_model, tokenizer, enum_decode, llm_client):
        self.overlay = overlay_model
        self.tokenizer = tokenizer
        self.enum_decode = enum_decode
        self.llm = llm_client

    def evaluate(self, context):
        text = "\n".join([
            "PROMPT: " + context["user_prompt"],
            "IRM: " + context["irm_state_digest"],
            "SCM: " + context["scm_state_digest"],
            "HISTORY: " + context["history_digest"],
            "DRAFT_REASONING: " + context["draft_reasoning"],
            "DRAFT_ANSWER: " + context["draft_answer"],
        ])

        enc = self.tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
        out = self.overlay(enc["input_ids"], enc["attention_mask"])

        decision = {
            "presence_integrity_score": float(out["presence_integrity_score"].item()),
            "drift_level": self.enum_decode["drift_level"](out["drift_logits"]),
            "collapse_mode": self.enum_decode["collapse_mode"](out["collapse_logits"]),
            "required_action": self.enum_decode["required_action"](out["action_logits"]),
        }
        return decision
