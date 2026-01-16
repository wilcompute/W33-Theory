import csv
import os
import subprocess
from pathlib import Path


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def test_eval_predictors_small(tmp_path):
    repo = Path(tmp_path)
    docs = repo / 'data' / '_docs'
    docs.mkdir(parents=True, exist_ok=True)

    # Create toe_key_lines.csv with a strong linear predictor and a null predictor
    rows = [
        ['line_id','native_mean_abs_delta','prior_score','node_commutator_score','mixed_score','e_star_oddness'],
        [1, 0.1, 0.1, 0.5, 0.2, 0.05],
        [2, 0.2, 0.2, 0.4, 0.1, 0.03],
        [3, 0.3, 0.3, 0.6, 0.0, 0.04],
        [4, 0.4, 0.4, 0.8, -0.1, 0.02],
        [5, 0.5, 0.5, 1.0, 0.0, 0.06],
    ]
    write_csv(docs / 'toe_key_lines.csv', rows[0], rows[1:])

    env = os.environ.copy()
    env['TOE_ROOT'] = str(repo)
    subprocess.check_call(['python', 'scripts/eval_predictors.py', '--permutations', '200', '--seed', '1'], env=env)

    out = docs / 'predictor_evaluation.csv'
    md = docs / 'predictor_evaluation.md'
    assert out.exists()
    assert md.exists()
    # read CSV and check that 'prior_score' shows substantial pearson
    import pandas as pd
    df = pd.read_csv(out)
    prior = df[df['predictor'] == 'prior_score'].iloc[0]
    assert prior['pearson'] > 0.9
    assert prior['pearson_p'] < 0.05
