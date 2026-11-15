"""Independent reproducible tests of apartment-frame sampling model."""
import importlib.util
import json
import math
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"toe_20261114_frame_fluctuation_sampling.py"

def module():
    spec=importlib.util.spec_from_file_location("frame_sampling",SRC)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def test_sample_reconstructs_every_relation_seeded():
    m=module()
    r=m.run()
    assert r["n_apartments"]==1620
    assert r["n_nonzero_displacements"]==80
    assert r["true_pair_counts"]=={"opposite":40,"orthogonal":960,"nonorthogonal":2160}
    assert r["misclassification_counts"]=={}
    assert r["empirical_accuracy"]==1

def test_Hoeffding_union_bound_arithmetic():
    r=module().run(n_samples=10000)
    assert r["Hoeffding_union_sufficient_frames_99pct_all_pairs"]==158972
    delta=(1/60-1/270)/2
    N=r["Hoeffding_union_sufficient_frames_99pct_all_pairs"]
    assert 2*3160*math.exp(-2*N*delta**2)<=.01
    assert 2*3160*math.exp(-2*(N-1)*delta**2)>.01

def test_random_sampling_replay_and_source_is_scoped():
    m=module()
    a=m.run(n_samples=10000,seed=20261114)
    b=m.run(n_samples=10000,seed=20261114)
    assert a["classified_pair_counts"]==b["classified_pair_counts"]
    assert a["status"]==b["status"]
    assert json.loads(m.OUT.read_text())["empirical_accuracy"]==1.0
    assert "not a 99% proof" in a["limits"]
