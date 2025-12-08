
import torch
import torch.nn as nn
from transformers import DistilBertModel

class PresenceOverlayClassifier(nn.Module):
    def __init__(self, num_labels):
        super().__init__()
        self.encoder = DistilBertModel.from_pretrained("distilbert-base-uncased")
        hidden = self.encoder.config.dim

        self.dropout = nn.Dropout(0.1)

        self.reg_head = nn.Linear(hidden, 1)
        self.drift_head = nn.Linear(hidden, num_labels["drift_level"])
        self.collapse_head = nn.Linear(hidden, num_labels["collapse_mode"])
        self.action_head = nn.Linear(hidden, num_labels["required_action"])

    def forward(self, input_ids, attention_mask):
        out = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        cls = self.dropout(out.last_hidden_state[:, 0, :])

        return {
            "presence_integrity_score": self.reg_head(cls).squeeze(-1),
            "drift_logits": self.drift_head(cls),
            "collapse_logits": self.collapse_head(cls),
            "action_logits": self.action_head(cls),
        }
