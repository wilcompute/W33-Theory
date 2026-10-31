import subprocess
import sys
import os

def run_script(name):
    path = os.path.join(os.getcwd(), name)
    result = subprocess.run([sys.executable, path], capture_output=True, text=True, encoding='utf-8', timeout=30)
    assert result.returncode == 0, f"Script {name} failed:\n{result.stdout}\n{result.stderr}"
    return result.stdout


def test_dm_mass_fit_runs():
    out = run_script('pillars/THEORY_PART_CLXII_DM_MASS_FIT.py')
    assert 'Best-fit DM mass' in out
    assert 'AMS-02' in out
