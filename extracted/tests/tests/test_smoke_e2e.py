import sys
import subprocess
import csv
from pathlib import Path

def write_csv(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in rows:
            writer.writerow(r)


def test_end_to_end_smoke(tmp_path):
    repo = tmp_path / 'repo'
    # create minimal repo layout expected by scripts
    ac_path = repo / 'data' / '_workbench' / '04_measurement' / 'action_candidate_features.csv'
    ph_path = repo / 'data' / '_workbench' / '02_geometry' / 'W33_line_phase_map.csv'

    write_csv(ac_path,
              ['line_id','native_mean_abs_delta','prior_score','fit_score','k12_entropy','k12_kl_global','tau_shift_similarity','var_q_r','var_q_class'],
              [[1,0.5,0.2,0.25,0.1,0.05,0.2,0.1,'A'], [2,0.1,0.15,0.05,0.2,0.02,0.1,0.0,'B'], [3,0.2,0.12,0.18,0.15,0.01,0.05,0.0,'A']])

    write_csv(ph_path,
              ['line_id','unique_k_mod6','unique_k_mod3'],
              [[1,2,1],[2,1,1]])

    # ensure docs dir exists (scripts expect data/_docs)
    (repo / 'data' / '_docs').mkdir(parents=True, exist_ok=True)

    python = sys.executable
    # Run generator
    subprocess.run([python, str(Path('scripts') / 'generate_toe_key_lines.py'), '--root', str(repo)], check=True)

    key_csv = repo / 'data' / '_docs' / 'toe_key_lines.csv'
    assert key_csv.exists(), 'toe_key_lines.csv was not created'

    # Run visualizer
    subprocess.run([python, str(Path('scripts') / 'visualize_toe_key_lines.py'), '--root', str(repo)], check=True)
    fig1 = repo / 'data' / '_docs' / 'figures' / 'prior_vs_native_scatter.png'
    fig2 = repo / 'data' / '_docs' / 'figures' / 'k12_entropy_hist.png'
    assert fig1.exists(), 'expected figure missing'
    assert fig2.exists(), 'expected figure missing'

    # Run evaluator with small permutation count
    subprocess.run([python, str(Path('scripts') / 'eval_predictors.py'), '--root', str(repo), '--permutations', '100', '--seed', '1'], check=True)
    eval_csv = repo / 'data' / '_docs' / 'predictor_evaluation.csv'
    assert eval_csv.exists(), 'predictor_evaluation.csv missing'

    # Check the evaluation csv has sensible content
    import pandas as pd
    df = pd.read_csv(eval_csv, encoding='utf-8-sig')
    assert not df.empty
    assert 'predictor' in df.columns
    finite_pear = df['pearson'].dropna()
    assert finite_pear.size > 0, 'No finite pearson values computed'
    assert finite_pear.apply(lambda v: -1.0 <= v <= 1.0).all()
