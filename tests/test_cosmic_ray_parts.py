import subprocess
import sys
import os

def run_script(name):
    path = os.path.join(os.getcwd(), name)
    # force utf-8 decoding to avoid CP1252 issues on Windows
    result = subprocess.run([sys.executable, path], capture_output=True, text=True, encoding='utf-8', timeout=30)
    assert result.returncode == 0, f"Script {name} failed:\n{result.stdout}\n{result.stderr}"


def test_clx_runs():
    run_script('pillars/THEORY_PART_CLX_COSMIC_RAY_DARK_SIGNALS.py')


def test_clxi_runs():
    run_script('pillars/THEORY_PART_CLXI_PROPAGATION_AND_FLUXES.py')
