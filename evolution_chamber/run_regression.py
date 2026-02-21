import yaml
from pathlib import Path
from multi_eye_probe import analyze


def check_case(case: dict):
    result = analyze(case["input"])
    exp = case.get("expected", {})

    ok = True

    if "required_layers" in exp:
        layers = [lid for lid, _ in result.get("structural_layers", [])]
        for req in exp["required_layers"]:
            ok &= (req in layers)

    if "grounding" in exp:
        ok &= (result["grounding"] == exp["grounding"])

    if "min_M3" in exp:
        ok &= (result["M3_score"] >= exp["min_M3"])

    if "min_M5" in exp:
        ok &= (result["M5_score"] >= exp["min_M5"])

    if "allowed_decisions" in exp:
        ok &= (result["decision"] in exp["allowed_decisions"])

    return ok, result


def main():
    suite_path = Path(__file__).parent / "MAE" / "scenarios" / "awareness_regression.yaml"
    with open(suite_path, "r", encoding="utf-8") as f:
        suite = yaml.safe_load(f)

    any_fail = False

    for case in suite["cases"]:
        ok, result = check_case(case)
        status = "PASS" if ok else "FAIL"
        any_fail |= (not ok)

        print(f"{status}: {case['id']}")
        print(f"  decision: {result['decision']}")
        print(f"  M3_score: {result['M3_score']}")
        print(f"  M5_score: {result['M5_score']}")

        if not ok:
            print(f"  expected: {case.get('expected')}")
            print(f"  actual:   decision={result['decision']}, M3={result['M3_score']}, M5={result['M5_score']}")
        print()

    if any_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()