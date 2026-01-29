from scripts.quantum_photonics.run_cv_repeater import sweep_repeater

def test_sweep_creates_output():
    data = sweep_repeater(r_values=[0.5], losses=[0.5])
    assert isinstance(data, list)
    assert len(data) == 1
    entry = data[0]
    assert 'ln_direct' in entry and 'ln_repeater_toy' in entry
    assert isinstance(entry['ln_direct'], float)
    assert isinstance(entry['ln_repeater_toy'], float)
