import sys
import shutil
import subprocess
from pathlib import Path
import pandas as pd

def test_eval_predictors_expanded_on_fixtures(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    fixtures = repo / 'data' / '_workbench' / '00_meta' / 'fixtures'

    r = tmp_path / 'repo'
    (r / 'data' / '_workbench' / '04_measurement').mkdir(parents=True)
    (r / 'data' / '_workbench' / '02_geometry').mkdir(parents=True)
    shutil.copy(fixtures / 'action_candidate_features_fixture.csv', r / 'data' / '_workbench' / '04_measurement' / 'action_candidate_features.csv')
    shutil.copy(fixtures / 'W33_line_phase_map_fixture.csv', r / 'data' / '_workbench' / '02_geometry' / 'W33_line_phase_map.csv')
    shutil.copy(fixtures / 'node_commutator_line_scores_fixture.csv', r / 'data' / '_workbench' / '04_measurement' / 'node_commutator_line_scores.csv')
    shutil.copy(fixtures / 'mixed_predictor_oddness_defect_scores_fixture.csv', r / 'data' / '_workbench' / '04_measurement' / 'mixed_predictor_oddness_defect_scores.csv')
    shutil.copy(fixtures / 'e_star_oddness_per_line_fixture.csv', r / 'data' / '_workbench' / '04_measurement' / 'e_star_oddness_per_line.csv')

    python = sys.executable
    subprocess.run([python, str(Path('scripts') / 'generate_toe_key_lines.py'), '--root', str(r)], check=True)
    subprocess.run([python, str(Path('scripts') / 'eval_predictors_expanded.py'), '--root', str(r), '--permutations', '100', '--seed', '1'], check=True)

    out_csv = r / 'data' / '_docs' / 'predictor_evaluation_expanded.csv'
    out_md = r / 'data' / '_docs' / 'predictor_evaluation_expanded.md'
    assert out_csv.exists()
    assert out_md.exists()

    df = pd.read_csv(out_csv, encoding='utf-8-sig')
    assert not df.empty
    assert 'predictor' in df.columns
    assert 'pearson_p_adj' in df.columns
