"""
Accuracy of the three models and of the combined system (X-ray CNN + Blood ANN + Oxygen ANN).

HOW THE NUMBERS ARE OBTAINED
- Each model is tested on ITS OWN held-out test set. The blood and oxygen test sets are rebuilt with
  exactly the same cleaning and train_test_split(test_size=0.2, random_state=42, stratify=y) used in the
  Colab training notebooks, so no training rows are used for testing.
- The three datasets come from different patients, so there is no real patient with all three inputs.
  The combined accuracy is therefore SIMULATED: each X-ray test image is paired with a random blood row
  and a random oxygen row of the same class (pneumonia/normal X-ray <-> abnormal/normal blood and oxygen),
  and the app's fusion rule (mean of the three probabilities, threshold 0.5) is applied. The pairing is
  repeated N_REPEATS times and the average is reported.
- Blood label = anemia (Hb cut-off) and oxygen label = SpO2 cut-off, so the combined figure is
  illustrative and optimistic. It is NOT clinical validation. Always call it "simulated".

Run from the Backend folder:  python evaluate_system.py
Results are printed and also saved to evaluation_results.txt
"""
import os
import numpy as np
import pandas as pd
import cv2
import joblib
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model

# ----------------------------- CONFIG (edit if needed) -----------------------------
IMG_SIZE = 224
XRAY_TEST_DIR = r"D:\chest_xray\test"             # contains NORMAL and PNEUMONIA folders
XRAY_MODEL = "final_model.keras"

BLOOD_DATA = "blood_count_dataset.csv"            # the ORIGINAL file; column A1 must be "Age"
BLOOD_MODEL, BLOOD_SCALER, BLOOD_FEATURES = "blood_model (3).h5", "blood_scaler (1).pkl", "blood_features.pkl"

OXYGEN_DATA = "Health data.csv"                    # the oxygen/vitals data file (csv or zip)
OXYGEN_MODEL, OXYGEN_SCALER = "oxygen_model (2).h5", "oxygen_scaler (1).pkl"

N_REPEATS = 100
SEED = 42
# -----------------------------------------------------------------------------------

REPORT = []


def say(text=""):
    print(text)
    REPORT.append(text)


def _require(path, config_name):
    if not os.path.exists(path):
        raise FileNotFoundError(f"'{os.path.abspath(path)}' not found. Set {config_name} in the CONFIG block.")


# ------------------------------------ X-ray ------------------------------------
def _class_dir(root, name):
    if not os.path.isdir(root):
        raise FileNotFoundError(f"X-ray test folder not found: '{root}'. Set XRAY_TEST_DIR.")
    for d in os.listdir(root):
        if d.lower() == name.lower() and os.path.isdir(os.path.join(root, d)):
            return os.path.join(root, d)
    raise FileNotFoundError(f"No '{name}' folder inside '{root}'. Found: {sorted(os.listdir(root))}")


def xray_probs():
    model = load_model(XRAY_MODEL)
    batch, labels = [], []
    for cls, y in (("NORMAL", 0), ("PNEUMONIA", 1)):
        folder = _class_dir(XRAY_TEST_DIR, cls)
        files = [f for f in os.listdir(folder) if f.lower().endswith((".jpeg", ".jpg", ".png"))]
        say(f"  X-ray {cls}: {len(files)} images")
        for f in files:
            img = cv2.imread(os.path.join(folder, f), cv2.IMREAD_COLOR)
            if img is None:
                continue
            batch.append(cv2.resize(img, (IMG_SIZE, IMG_SIZE)).astype("float32") / 255.0)
            labels.append(y)
    if not batch:
        raise FileNotFoundError("No X-ray images were found.")
    probs = model.predict(np.array(batch), batch_size=32, verbose=0).ravel()
    return probs, np.array(labels)


# ------------------------------------ Blood ------------------------------------
def blood_probs():
    _require(BLOOD_DATA, "BLOOD_DATA")
    df = pd.read_csv(BLOOD_DATA)
    if df.columns[0] != "Age":
        say(f"  WARNING: first blood column is '{df.columns[0]}', renamed to 'Age'. Check the original CSV.")
        df = df.rename(columns={df.columns[0]: "Age"})

    # Same cleaning and labelling as the blood training notebook
    df = df.dropna().drop_duplicates().reset_index(drop=True)
    df["Gender"] = df["Gender"].str.strip().str.lower().map({"male": 1, "female": 0})
    features = list(joblib.load(BLOOD_FEATURES))
    say(f"  Blood features used by the model: {features}")
    y = (df["Hemoglobin"] < np.where(df["Gender"] == 1, 13, 12)).astype(int).values   # anemia label
    X = df[features].values

    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model, scaler = load_model(BLOOD_MODEL), joblib.load(BLOOD_SCALER)
    out = np.asarray(model.predict(scaler.transform(X_test), verbose=0))
    probs = out[:, -1] if out.ndim == 2 else out.ravel()
    return probs, y_test.astype(int)


# ------------------------------------ Oxygen ------------------------------------
def oxygen_probs():
    _require(OXYGEN_DATA, "OXYGEN_DATA")
    df = pd.read_csv(OXYGEN_DATA).dropna().drop_duplicates()
    needed = ["pulse", "body temperature", "SpO2"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Oxygen file is missing column(s) {missing}. Columns found: {list(df.columns)}")
    X = df[["pulse", "body temperature", "SpO2"]].values
    y = np.where(df["SpO2"] >= 95, 0, np.where(df["SpO2"] >= 90, 1, 2)).astype(int)   # 0/1/2 as in notebook

    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model, scaler = load_model(OXYGEN_MODEL), joblib.load(OXYGEN_SCALER)
    p = np.asarray(model.predict(scaler.transform(X_test), verbose=0))
    acc3 = float((p.argmax(axis=1) == y_test).mean())
    say(f"  Oxygen 3-class accuracy (Normal / Low / Very low): {acc3:.3f}  (n={len(y_test)})")
    return 1.0 - p[:, 0], (y_test != 0).astype(int)        # P(abnormal), abnormal = class 1 or 2


# ------------------------------------ Metrics ------------------------------------
def metrics(y_true, y_pred):
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    return {"accuracy": (tp + tn) / max(tp + tn + fp + fn, 1),
            "sensitivity": tp / max(tp + fn, 1),
            "specificity": tn / max(tn + fp, 1),
            "precision": tp / max(tp + fp, 1)}


def main():
    rng = np.random.default_rng(SEED)
    results = {}

    say("Loading and testing each model on its own test set")
    for name, loader in (("X-ray", xray_probs), ("Blood", blood_probs), ("Oxygen", oxygen_probs)):
        try:
            results[name] = loader()
        except Exception as e:
            say(f"  {name} skipped: {e}")

    say("\nIndividual models (own test sets, threshold 0.5)")
    for name, (p, y) in results.items():
        m = metrics(y, (p > 0.5).astype(int))
        say(f"  {name:7s} accuracy={m['accuracy']:.3f}  sensitivity={m['sensitivity']:.3f}  "
            f"specificity={m['specificity']:.3f}  (n={len(y)})")

    if len(results) < 3:
        say("\nCombined system not calculated: all three models are needed.")
    else:
        x_p, x_y = results["X-ray"]
        b_p, b_y = results["Blood"]
        o_p, o_y = results["Oxygen"]
        pools = {c: (b_p[b_y == c], o_p[o_y == c]) for c in (0, 1)}

        runs = []
        for _ in range(N_REPEATS):
            blood_s = np.empty(len(x_y))
            oxy_s = np.empty(len(x_y))
            for c in (0, 1):
                idx = np.where(x_y == c)[0]
                blood_s[idx] = rng.choice(pools[c][0], size=len(idx), replace=True)
                oxy_s[idx] = rng.choice(pools[c][1], size=len(idx), replace=True)
            fused = (x_p + blood_s + oxy_s) / 3.0                       # same rule as the web app
            runs.append(metrics(x_y, (fused >= 0.5).astype(int)))

        say(f"\nCOMBINED SYSTEM - SIMULATED pairing ({N_REPEATS} random pairings, n={len(x_y)} X-ray test cases)")
        for k in ("accuracy", "sensitivity", "specificity", "precision"):
            v = np.array([r[k] for r in runs])
            say(f"  {k:12s} {v.mean():.3f} +/- {v.std():.3f}")
        say("\nNote: simulated and optimistic (blood label = anemia, oxygen label = SpO2 cut-off).")

    with open("evaluation_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(REPORT))
    print("\nSaved to evaluation_results.txt")


if __name__ == "__main__":
    main()