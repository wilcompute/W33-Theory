import csv
import os
import subprocess
from pathlib import Path
import tempfile
import pytest


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def test_generate_toe_key_lines_basic(tmp_path, monkeypatch):
    # Create a minimal repo layout under tmp_path
    repo = Path(tmp_path)
    ac_path = repo / 'data' / '_workbench' / '04_measurement' / 'action_candidate_features.csv'
    ph_path = repo / 'data' / '_workbench' / '02_geometry' / 'W33_line_phase_map.csv'

    # Minimal action candidate file
    write_csv(ac_path, ['line_id', 'native_mean_abs_delta', 'k12_entropy', 'prior_score', 'fit_score'],
              [[1, 0.5, 0.1, 0.2, 0.3], [2, 1.5, 0.2, 0.4, 0.6]])

    # Minimal phase map
    write_csv(ph_path, ['line_id', 'unique_k_mod6', 'unique_k_mod3'], [[1, 2, 1], [2, 3, 0]])

    # Run the generator with TOE_ROOT pointing to the tmp repo
    env = os.environ.copy()
    env['TOE_ROOT'] = str(repo)
    subprocess.check_call(['python', 'scripts/generate_toe_key_lines.py'], env=env)

    out = repo / 'data' / '_docs' / 'toe_key_lines.csv'
    assert out.exists()

    # Verify columns and content
    with open(out, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2
    assert 'line_id' in reader.fieldnames
    # Predictor fields should be present even if predictors were not provided
    assert 'mixed_score' in reader.fieldnames
    assert 'e_star_oddness' in reader.fieldnames


def test_generate_toe_key_lines_with_predictors(tmp_path):
    repo = Path(tmp_path)
    (repo / 'data' / '_workbench' / '04_measurement').mkdir(parents=True)

    # create action_candidate + phase files
    write_csv(repo / 'data' / '_workbench' / '04_measurement' / 'action_candidate_features.csv',
              ['line_id', 'native_mean_abs_delta', 'k12_entropy', 'prior_score', 'fit_score'],
              [[1, 0.5, 0.1, 0.2, 0.3]])
    write_csv(repo / 'data' / '_workbench' / '02_geometry' / 'W33_line_phase_map.csv',
              ['line_id', 'unique_k_mod6', 'unique_k_mod3'], [[1, 2, 1]])

    # create node and mixed and e* predictor files
    write_csv(repo / 'data' / '_workbench' / '04_measurement' / 'node_commutator_line_scores.csv',
              ['line_id', 'score'], [[1, 0.7]])
    write_csv(repo / 'data' / '_workbench' / '04_measurement' / 'mixed_predictor_oddness_defect_scores.csv',
              ['line_id', 'score'], [[1, 0.2]])
    write_csv(repo / 'data' / '_workbench' / '04_measurement' / 'e_star_oddness_per_line.csv',
              ['line_id', 'odd_fraction'], [[1, 0.123]])

    env = os.environ.copy()
    env['TOE_ROOT'] = str(repo)
    subprocess.check_call(['python', 'scripts/generate_toe_key_lines.py'], env=env)

    out = repo / 'data' / '_docs' / 'toe_key_lines.csv'
    with open(out, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 1
    row = rows[0]
    assert float(row['node_commutator_score']) == pytest.approx(0.7)
    assert float(row['mixed_score']) == pytest.approx(0.2)
    assert float(row['e_star_oddness']) == pytest.approx(0.123)
