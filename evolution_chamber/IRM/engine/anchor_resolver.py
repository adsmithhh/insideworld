def classify_conflict(b, inj):
    diffs = {}
    for k,v in (inj or {}).items():
        if b.get(k) != v:
            diffs[k] = (b.get(k), v)

    n = len(diffs)
    if n == 0:
        return "none", diffs
    if n == 1:
        return "mild", diffs
    if n <= 3:
        return "strong", diffs
    return "catastrophic", diffs

def resolve(b, inj, diffs):
    """
    Resolution: keep originals unless injection overrides.
    """
    newA = dict(b)
    for k,(old,new) in diffs.items():
        newA[k] = new
    return newA
