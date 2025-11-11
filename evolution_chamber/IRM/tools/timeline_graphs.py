import os, yaml
import matplotlib.pyplot as plt

ROOT  = os.path.abspath(os.path.join(__file__, "..", ".."))
INOUT = os.path.join(ROOT, "inout.yaml")
OUT   = os.path.join(ROOT, "timeline_graphs")
os.makedirs(OUT, exist_ok=True)

def load_inout():
    with open(INOUT,"r",encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    d = load_inout()["inout"]
    T = [e["t"] for e in d["timeline"]]
    drift = [e["drift_norm"] for e in d["timeline"]]
    f1 = [e.get("continuity_f1",1) for e in d["timeline"]]
    notes = [e["notes"] for e in d["timeline"]]

    # drift graph
    plt.figure()
    plt.plot(T, drift)
    plt.title("Drift Norm over Time")
    plt.xlabel("t")
    plt.ylabel("drift_norm")
    plt.savefig(os.path.join(OUT,"drift_norm.png"))
    plt.close()

    # continuity graph
    plt.figure()
    plt.plot(T, f1)
    plt.title("Continuity F1 over Time")
    plt.xlabel("t")
    plt.ylabel("F1 score")
    plt.savefig(os.path.join(OUT,"continuity_f1.png"))
    plt.close()

    print("[OK] graphs written to", OUT)

if __name__ == "__main__":
    main()
