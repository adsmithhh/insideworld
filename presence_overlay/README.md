
# Presence Overlay — Classifier-Based Regulator

This module implements a classifier-style micro-model used to regulate a large LLM
through Presence / Multi-Eye / IRM/SCM doctrines.

Model family: DistilBERT (option B)
Capabilities:
- drift detection
- collapse mode detection
- presence-integrity scoring
- required_action classification (allow / revise / reject / escalate)

Training data must follow dataset_entry schema.

Folder structure:

configs/         — YAML configs for kernel + training  
data/raw/        — manually created dataset entries  
data/processed/  — merged train/val/test YAML files  
src/             — Python scripts (dataset, model, training, orchestration)  
models/          — base + checkpoints  
logs/            — training logs  

This module is standalone and does NOT modify upstream model kernels.
