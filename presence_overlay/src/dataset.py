
import yaml
from torch.utils.data import Dataset

class PresenceOverlayDataset(Dataset):
    def __init__(self, path, tokenizer, max_len=512, enum_maps=None):
        with open(path, "r", encoding="utf-8") as f:
            self.entries = list(yaml.safe_load_all(f))
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.enum_maps = enum_maps

    def _compose_text(self, entry):
        ib = entry["input_bundle"]
        parts = [
            "PROMPT: " + ib["user_prompt"],
            "IRM: " + ib.get("irm_state_digest", ""),
            "SCM: " + ib.get("scm_state_digest", ""),
            "HISTORY: " + ib.get("history_digest", ""),
            "DRAFT_REASONING: " + ib.get("draft_reasoning", ""),
            "DRAFT_ANSWER: " + ib.get("draft_answer", "")
        ]
        return "\n".join(parts)

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, idx):
        entry = self.entries[idx]
        text = self._compose_text(entry)
        labels = entry["label_bundle"]

        enc = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )

        item = {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "presence_integrity_score": float(labels["presence_integrity_score"]),
            "drift_level": self.enum_maps["drift_level"][labels["drift_level"]],
            "collapse_mode": self.enum_maps["collapse_mode"][labels["collapse_mode"]],
            "required_action": self.enum_maps["required_action"][labels["required_action"]],
        }
        return item
