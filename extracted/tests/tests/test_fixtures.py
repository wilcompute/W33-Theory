import sys
import shutil
import subprocess
from pathlib import Path
import csv


def test_fixtures_exist():
    repo = Path(__file__).resolve().parents[1]
    fixtures = repo / 'data' / '_workbench' / '00_meta' / 'fixtures'
    expected = [
        'action_candidate_features_fixture.csv',
        'W33_line_phase_map_fixture.csv',
        'node_commutator_line_scores_fixture.csv',
        'mixed_predictor_oddness_defect_scores_fixture.csv',
        'e_star_oddness_per_line_fixture.csv',
    ]
    for f in expected:
        p = fixtures / f
        assert p.exists(), f'Missing fixture {p}'


def test_generate_from_fixtures(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    fixtures = repo / 'data' / '_workbench' / '00_meta' / 'fixtures'

    # create a temporary repo structure and copy fixtures into expected locations
    r = tmp_path / 'repo'
    (r / 'data' / '_workbench' / '04_measurement').mkdir(parents=True)
    (r / 'data' / '_workbench' / '02_geometry').mkdir(parents=True)
    shutil.copy(fixtures / 'action_candidate_features_fixture.csv', r / 'data' / '_workbench' / '04_measurement' / 'action_candidate_features.csv')
    shutil.copy(fixtures / 'W33_line_phase_map_fixture.csv', r / 'data' / '_workbench' / '02_geometry' / 'W33_line_phase_map.csv')
    shutil.copy(fixtures / 'node_commutator_line_scores_fixture.csv', r / 'data' / '_workbench' / '04_measurement' / 'node_commutator_line_scores.csv')
    shutil.copy(fixtures / 'mixed_predictor_oddness_defect_scores_fixture.csv', r / 'data' / '_workbench' / '04_measurement' / 'mixed_predictor_oddness_defect_scores.csv')
    shutil.copy(fixtures / 'e_star_oddness_per_line_fixture.csv', r / 'data' / '_workbench' / '04_measurement' / 'e_star_oddness_per_line.csv')

    python = sys.executable
    # run generator
    subprocess.run([python, str(Path('scripts') / 'generate_toe_key_lines.py'), '--root', str(r)], check=True)
    # run visualizer
    subprocess.run([python, str(Path('scripts') / 'visualize_toe_key_lines.py'), '--root', str(r)], check=True)
    # run eval_predictors with small perms
    subprocess.run([python, str(Path('scripts') / 'eval_predictors.py'), '--root', str(r), '--permutations', '100', '--seed', '1'], check=True)

    # check outputs
    assert (r / 'data' / '_docs' / 'toe_key_lines.csv').exists()
    assert (r / 'data' / '_docs' / 'figures' / 'prior_vs_native_scatter.png').exists()
    assert (r / 'data' / '_docs' / 'predictor_evaluation.csv').exists()

    # quick content check
    import pandas as pd
    df = pd.read_csv(r / 'data' / '_docs' / 'predictor_evaluation.csv', encoding='utf-8-sig')
    assert not df.empty
    assert 'predictor' in df.columns
