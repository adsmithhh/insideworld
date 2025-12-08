
import yaml, torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, get_linear_schedule_with_warmup
from dataset import PresenceOverlayDataset
from model_classifier import PresenceOverlayClassifier

def train(config_path="configs/train_classifier.yaml"):
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(cfg["model"]["base"])

    enum_maps = {
        "drift_level": {"none":0,"mild":1,"moderate":2,"severe":3},
        "collapse_mode": {"none":0,"compliance":1,"superficial":2,"evasive":3,"contradiction_blind":4},
        "required_action": {"allow":0,"revise":1,"reject":2,"escalate":3},
    }

    train_ds = PresenceOverlayDataset(cfg["data"]["train_path"], tokenizer, cfg["model"]["max_seq_len"], enum_maps)
    val_ds = PresenceOverlayDataset(cfg["data"]["val_path"], tokenizer, cfg["model"]["max_seq_len"], enum_maps)

    train_loader = DataLoader(train_ds, batch_size=cfg["training"]["batch_size"], shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=cfg["training"]["batch_size"])

    model = PresenceOverlayClassifier(cfg["model"]["num_labels"]).to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg["training"]["learning_rate"])
    ce = torch.nn.CrossEntropyLoss()
    mse = torch.nn.MSELoss()

    for epoch in range(cfg["training"]["num_epochs"]):
        model.train()
        for batch in train_loader:
            optimizer.zero_grad()

            out = model(batch["input_ids"].to(device), batch["attention_mask"].to(device))

            loss = (
                mse(out["presence_integrity_score"], batch["presence_integrity_score"].to(device))
                + ce(out["drift_logits"], batch["drift_level"].to(device))
                + ce(out["collapse_logits"], batch["collapse_mode"].to(device))
                + ce(out["action_logits"], batch["required_action"].to(device))
            )

            loss.backward()
            optimizer.step()

        torch.save(model.state_dict(), cfg["training"]["checkpoint_dir"] + "/epoch_" + str(epoch) + ".pt")
