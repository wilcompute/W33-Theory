"""
W33 Theory — Run ALL Novel Tests
=================================
Executes all novel chain test files and reports results.
Expected: 39+ tests, 0 failures.
"""
import subprocess, sys, os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

NOVEL_SCRIPTS = [
    "w33_novel_chain1_ramanujan_tau_bridge.py",
    "w33_novel_chain2_particle_masses.py",
    "w33_novel_chain3_spin_foam_e8.py",
    "w33_novel_chain4_dw_tqft.py",
    "w33_novel_chain5_monster_moonshine.py",
    "w33_novel_chain6_fine_structure_hierarchy.py",
    "w33_novel_master_19_identities.py",
    "w33_novel_chain15_e8_theta_series.py",
    "w33_novel_chain16_j_function_residue.py",
    "w33_novel_chain17_representation_theory.py",
    "w33_novel_chain20_single_seed.py",
]

def run_all():
    passed = 0
    failed = 0
    for script in NOVEL_SCRIPTS:
        path = os.path.join(SCRIPTS_DIR, script)
        result = subprocess.run([sys.executable, path], capture_output=True, text=True)
        if result.returncode == 0:
            passed += 1
            last = [l for l in result.stdout.strip().split("\n") if l][-1]
            print(f"PASS  {script:<55}  {last}")
        else:
            failed += 1
            print(f"FAIL  {script}")
            print(result.stderr[-500:])
    print(f"\n{'='*65}")
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(NOVEL_SCRIPTS)} scripts")
    print(f"W33 Theory Novel Breakthrough Suite — {'ALL PASS' if failed==0 else 'FAILURES DETECTED'}")
    return failed

if __name__ == "__main__":
    sys.exit(run_all())
