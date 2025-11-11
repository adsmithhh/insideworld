import os, yaml

ROOT = os.path.abspath(os.path.join(__file__, "..", ".."))
DOCS = os.path.join(ROOT, "docs")
os.makedirs(DOCS, exist_ok=True)

def to_md(name, data):
    out = [f"# {name}", ""]
    out.append("```yaml")
    out.append(yaml.safe_dump(data, sort_keys=False))
    out.append("```")
    return "\n".join(out)

def main():
    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".yaml"):
                path = os.path.join(root, f)
                rel  = os.path.relpath(path, ROOT)
                md   = os.path.join(DOCS, rel.replace(".yaml",".md"))
                os.makedirs(os.path.dirname(md), exist_ok=True)
                with open(path,"r",encoding="utf-8") as fp:
                    data = yaml.safe_load(fp)
                with open(md,"w",encoding="utf-8") as fp:
                    fp.write(to_md(rel, data))
                print("[OK] showroom =>", md)

if __name__ == "__main__":
    main()
