"""
fusion.py - corrected Stage-1 decision fusion for the Pneumonia Detection System.

Replaces the old combine_stage1() / display_headline() in main.py.

Rules (in priority order)
  1. X-ray CNN is the primary modality.
        P >= 0.80  -> LIKELY      (never reported as "no signs", whatever the other models say)
        P >= 0.50  -> POSSIBLE
  2. Blood ANN >= 0.50 with a negative X-ray -> POSSIBLE.
  3. Strong model disagreement on an otherwise negative case -> INCONCLUSIVE.
  4. Otherwise -> NEGATIVE.
The shown score is ONE number: a weighted pneumonia likelihood (X-ray weighted highest,
partial blood profile down-weighted). Blood/Oxygen models can raise concern but never
override a positive X-ray.
"""

# ---- tunable settings (validate on a labelled set before clinical use) ----
XRAY_HIGH = 0.80
XRAY_POSSIBLE = 0.50
OTHER_POSSIBLE = 0.50
DISAGREE_GAP = 0.50

W_XRAY = 0.60
W_BLOOD = 0.25
W_OXYGEN = 0.15
PARTIAL_BLOOD_FACTOR = 0.5   # blood profile is partial (MCV/MCH/MCHC imputed) -> half weight

LIKELY, POSSIBLE, INCONCLUSIVE, NEGATIVE = "LIKELY", "POSSIBLE", "INCONCLUSIVE", "NEGATIVE"

_DB_LABEL = {LIKELY: "PNEUMONIA DETECTED", POSSIBLE: "PNEUMONIA POSSIBLE",
             INCONCLUSIVE: "INCONCLUSIVE", NEGATIVE: "NORMAL"}
_DISPLAY_LABEL = {LIKELY: "PNEUMONIA SUSPECTED", POSSIBLE: "POSSIBLE PNEUMONIA",
                  INCONCLUSIVE: "INCONCLUSIVE", NEGATIVE: "NO PNEUMONIA PATTERN"}
_FINAL_TEXT = {LIKELY: "Pneumonia suspected", POSSIBLE: "Possible pneumonia",
               INCONCLUSIVE: "Inconclusive", NEGATIVE: "Normal"}


def combine_stage1(cnn_p, blood_result, oxygen_result):
    components, probs, weights = [], {}, {}

    xray_positive = cnn_p >= XRAY_POSSIBLE
    components.append({
        "name": "X-ray CNN", "available": True, "is_positive": xray_positive,
        "result": "Positive" if xray_positive else "Normal",
        "detail": f"P(pneumonia) {cnn_p * 100:.1f}%",
    })
    probs["xray"], weights["xray"] = cnn_p, W_XRAY

    blood_p = None
    if blood_result.get("available"):
        blood_p = blood_result["prob"]
        components.append({
            "name": "Blood ANN", "available": True, "is_positive": blood_p >= OTHER_POSSIBLE,
            "result": "Positive" if blood_p >= OTHER_POSSIBLE else "Normal",
            "detail": f"P(pneumonia) {blood_p * 100:.1f}% (partial profile, reduced weight)",
        })
        probs["blood"] = blood_p
        weights["blood"] = W_BLOOD * (PARTIAL_BLOOD_FACTOR if blood_result.get("partial_profile") else 1.0)
    else:
        components.append({"name": "Blood ANN", "available": False, "is_positive": None,
                           "result": "Not assessed", "detail": blood_result.get("reason", "")})

    if oxygen_result.get("available"):
        components.append({
            "name": "Oxygen ANN", "available": True,
            "is_positive": oxygen_result["p_pos"] >= 0.5,
            "result": "Positive" if oxygen_result["p_pos"] >= 0.5 else "Normal",
            "detail": (f"{oxygen_result.get('class_label', '')} - "
                       f"P(abnormal vitals) {oxygen_result['p_pos'] * 100:.1f}%"),
        })
        probs["oxygen"], weights["oxygen"] = oxygen_result["p_pos"], W_OXYGEN
    else:
        components.append({"name": "Oxygen ANN", "available": False, "is_positive": None,
                           "result": "Not assessed", "detail": oxygen_result.get("reason", "")})

    # single, consistent score: weighted pneumonia likelihood
    final_p = sum(weights[k] * probs[k] for k in probs) / sum(weights.values())
    spread = max(probs.values()) - min(probs.values()) if len(probs) > 1 else 0.0

    reasons = []
    driver = "xray"          # which signal produced a positive/possible verdict
    if cnn_p >= XRAY_HIGH:
        verdict = LIKELY
        reasons.append(f"X-ray model strongly suggests pneumonia ({cnn_p * 100:.1f}%).")
    elif cnn_p >= XRAY_POSSIBLE:
        verdict = POSSIBLE
        reasons.append(f"X-ray model suggests pneumonia ({cnn_p * 100:.1f}%).")
    elif blood_p is not None and blood_p >= OTHER_POSSIBLE:
        verdict = POSSIBLE
        driver = "blood"
        reasons.append(f"Blood model suggests pneumonia ({blood_p * 100:.1f}%) despite a normal X-ray.")
    elif spread >= DISAGREE_GAP:
        verdict = INCONCLUSIVE
        reasons.append("Models disagree strongly; the result cannot be relied on.")
    else:
        verdict = NEGATIVE
        reasons.append("No model flagged a pneumonia pattern.")

    is_positive = verdict in (LIKELY, POSSIBLE)
    # disagreement = any available model sits on the other side of 0.5 from the X-ray
    disagree = any((p >= 0.5) != xray_positive for p in probs.values())
    if disagree and is_positive:
        reasons.append("Other checks did not support the X-ray result; this does not lower the need for review.")

    components.append({
        "name": "Final Result", "available": True, "is_positive": is_positive,
        "verdict": verdict, "driver": driver, "result": _FINAL_TEXT[verdict],
        "detail": f"Pneumonia likelihood {final_p * 100:.1f}% (weighted, X-ray highest weight)",
    })

    return {
        "is_positive": is_positive,       # LIKELY or POSSIBLE -> drives severity staging
        "xray_positive": xray_positive,   # drives Grad-CAM / bounding box / image
        "verdict": verdict,
        "driver": driver,
        "label": _DB_LABEL[verdict],      # stored in DB only
        "display_label": _DISPLAY_LABEL[verdict],   # wording shown in reports (never "detected")
        "final_prob": final_p,
        "confidence": final_p * 100,      # the ONE score shown everywhere
        "n_models": len(probs),
        "disagree": disagree,
        "reasons": reasons,
        "components": components,
    }


def headline_for(stage1, urgent_override=False):
    v = stage1["verdict"]
    if v == LIKELY:
        return "PNEUMONIA SUSPECTED"
    if v == POSSIBLE:
        if stage1.get("driver") == "blood":
            return "X-RAY LOOKS NORMAL \u2013 ABNORMAL BLOOD RESULTS, DOCTOR REVIEW ADVISED"
        return "POSSIBLE PNEUMONIA \u2013 DOCTOR REVIEW ADVISED"
    if v == INCONCLUSIVE:
        return "RESULT INCONCLUSIVE \u2013 DOCTOR REVIEW REQUIRED"
    if urgent_override:
        return "NO PNEUMONIA PATTERN \u2013 URGENT MEDICAL REVIEW ADVISED"
    return "NO SIGNS OF PNEUMONIA FOUND"


def result_class_for(stage1, urgent_override=False):
    v = stage1["verdict"]
    if v == LIKELY:
        return "positive"
    if v in (POSSIBLE, INCONCLUSIVE) or urgent_override:
        return "caution"
    return "negative"


if __name__ == "__main__":
    ok = {"available": True, "p_pos": 0.004, "class_label": "Normal"}
    # Your screenshot case
    r = combine_stage1(0.987, {"available": True, "prob": 0.001, "partial_profile": True}, ok)
    assert r["verdict"] == LIKELY and r["is_positive"] and r["xray_positive"]
    print(headline_for(r), f"| likelihood {r['confidence']:.1f}%", "| disagree:", r["disagree"])
    # Clean negative
    r = combine_stage1(0.05, {"available": True, "prob": 0.04, "partial_profile": True}, ok)
    assert r["verdict"] == NEGATIVE and not r["disagree"]
    # Blood positive, X-ray negative
    r = combine_stage1(0.10, {"available": True, "prob": 0.90, "partial_profile": True}, ok)
    assert r["verdict"] == POSSIBLE
    # X-ray borderline positive
    assert combine_stage1(0.60, {"available": False}, {"available": False})["verdict"] == POSSIBLE
    print("fusion.py checks passed")