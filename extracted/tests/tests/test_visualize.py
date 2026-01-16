import os
import csv
import subprocess
from pathlib import Path

def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def test_visualizer_writes_figures(tmp_path):
    repo = Path(tmp_path)
    docs = repo / 'data' / '_docs'
    docs.mkdir(parents=True, exist_ok=True)
    # create a minimal toe_key_lines.csv
    write_csv(docs / 'toe_key_lines.csv', ['line_id', 'native_mean_abs_delta', 'prior_score', 'k12_entropy', 'unique_k_mod6'],
              [[1, 0.5, 0.2, 0.1, 2], [2, 1.2, 0.6, 0.5, 3]])

    env = os.environ.copy()
    env['TOE_ROOT'] = str(repo)
    subprocess.check_call(['python', 'scripts/visualize_toe_key_lines.py'], env=env)

    fig1 = docs / 'figures' / 'prior_vs_native_scatter.png'
    fig2 = docs / 'figures' / 'k12_entropy_hist.png'
    assert fig1.exists()
    assert fig2.exists()
