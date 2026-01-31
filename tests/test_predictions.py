import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PRED_PATH = ROOT / "data" / "predictions.json"
REF_PATH = ROOT / "tests" / "reference_values.json"


@pytest.fixture(scope="module")
def predictions():
    with open(PRED_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="module")
def references():
    with open(REF_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


@pytest.mark.parametrize(
    "key", ["H0_CMB", "H0_local", "alpha_inv", "sin2_theta_w", "M_Higgs_GeV"]
)
def test_prediction_with_reference(key, predictions, references):
    assert key in predictions, f"Missing prediction for {key}"
    assert key in references, f"Missing reference for {key}"

    pred = predictions[key]["value"]
    pred_tol = float(predictions[key].get("tolerance", 0))

    ref = references[key]["value"]
    ref_unc = float(references[key].get("uncertainty", 0))

    # Accept if within either declared prediction tolerance OR within 3σ of reference
    allowed = max(pred_tol, 3 * ref_unc)
    diff = abs(pred - ref)

    assert diff <= allowed, (
        f"Prediction {key}={pred} differs from reference {ref} by {diff}, "
        f"allowed {allowed}. See data/predictions.json and tests/reference_values.json"
    )
