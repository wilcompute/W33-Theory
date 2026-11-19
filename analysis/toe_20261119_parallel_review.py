"""Replay the Nov18/19 parallel packet without overwriting its certificates.

All producer writes to repo/data are redirected to a temporary directory.
The two subprocess-based tests are run in-process under that same redirection.
This is regression replay, not independent proof of all mathematical claims.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = [
    '20261118_fivefront_global_physics_closure',
    '20261118_sixfront_global_center_morse_selection',
    '20261118_native_E8_C9_link_SU5_G2_qutrit',
    '20261118_E8_full248_Psi_relative_G2_localMUB',
    '20261118_chirality_anomaly_FRflux_Markov_equivariant',
    '20261118_H27_G2_flat_Higgs_qutrit_break',
    '20261118_H27_Einstein_Hesse_E8_Higgs_PW_GHZ',
    '20261118_H27_S5T2_G2_sextic_center_sequential',
    '20261119_sic_moment_map_audit',
    '20261119_sic_baryon_plucker_alignment',
    '20261119_h27_integral_torsion_gerbes',
    '20261119_h27_clifford_torsion_clock',
    '20261118_six_front_research',
    '20261119_five_frontier_bridge',
    '20261119_w33_40_qutrit_css',
    '20261119_five_front_research',
]
EXTRA = ['20261118_susy_sic_uv_completion',
         '20261118_four_independent_bottleneck_probes',
         '20261119_h27_integral_torsion_gerbes',
         '20261119_h27_clifford_torsion_clock',
         '20261119_five_frontier_bridge', '20261119_w33_40_qutrit_css',
         '20261119_four_structural_frontier_tests',
         '20261119_w33_code_gate_and_decoder']


def differences(a, b, path='$'):
    if type(a) != type(b):
        return [path]
    if isinstance(a, dict):
        return ([path + '.keys'] if a.keys() != b.keys() else []) + [
            p for k in a.keys() & b.keys() for p in differences(a[k], b[k], path+'.'+str(k))]
    if isinstance(a, list):
        return ([path+'.length'] if len(a) != len(b) else []) + [
            p for i, (x, y) in enumerate(zip(a, b)) for p in differences(x, y, path+f'[{i}]')]
    return [] if a == b else [path]


def run():
    original_write, original_read, original_subprocess = Path.write_text, Path.read_text, subprocess.run
    captured, original_hashes = {}, {}
    stream = io.StringIO()
    with tempfile.TemporaryDirectory(prefix='toe_parallel_review_') as temporary:
        def mapped(p):
            p = p.resolve()
            return Path(temporary)/p.name if p.parent == (ROOT/'data').resolve() else None

        def write(p, content, *args, **kwargs):
            destination = mapped(p)
            if destination is None:
                raise AssertionError(f'Unexpected producer write: {p}')
            key = str(p.resolve())
            if key not in original_hashes:
                original_hashes[key] = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
            captured[key] = destination
            return original_write(destination, content, *args, **kwargs)

        def read(p, *args, **kwargs):
            destination = mapped(p)
            return original_read(destination if destination and destination.exists() else p, *args, **kwargs)

        def child(args, *other, **kwargs):
            if (isinstance(args, (list, tuple)) and len(args) == 2
                    and Path(args[1]).name in {
                        'toe_20261119_sic_moment_map_audit.py',
                        'toe_20261119_sic_baryon_plucker_alignment.py'}):
                output, errors = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                    runpy.run_path(str(args[1]), run_name='__main__')
                return subprocess.CompletedProcess(args, 0, output.getvalue(), errors.getvalue())
            return original_subprocess(args, *other, **kwargs)

        try:
            Path.write_text, Path.read_text, subprocess.run = write, read, child
            suite = unittest.TestSuite()
            with contextlib.redirect_stdout(stream):
                for name in NAMES:
                    path = ROOT/'tests'/f'test_toe_{name}.py'
                    spec = importlib.util.spec_from_file_location('review_'+name, path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
                result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
                for name in EXTRA:
                    runpy.run_path(str(ROOT/'analysis'/f'toe_{name}.py'), run_name='__main__')
        finally:
            Path.write_text, Path.read_text, subprocess.run = original_write, original_read, original_subprocess
        comparisons = []
        for key, destination in sorted(captured.items()):
            source = Path(key)
            assert hashlib.sha256(source.read_bytes()).hexdigest() == original_hashes[key], key
            a = json.loads(original_read(source, encoding='utf-8'))
            b = json.loads(original_read(destination, encoding='utf-8'))
            delta = sorted(differences(a, b))
            comparisons.append({'path':source.relative_to(ROOT).as_posix(),
                                'original_sha256':original_hashes[key],
                                'exact_structural_match':not delta, 'differing_paths':delta})
        receipt = {'status':'PASS' if result.wasSuccessful() else 'FAIL',
                   'scope':'Regression replay; does not independently prove every theorem or the TOE.',
                   'test_modules':NAMES, 'tests_run':result.testsRun,
                   'failures':len(result.failures), 'errors':len(result.errors),
                   'parallel_data_files_unchanged':len(comparisons), 'comparisons':comparisons,
                   'test_output':stream.getvalue()}
    target = ROOT/'data/toe_20261119_parallel_review.json'
    target.write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('comparisons','test_output','test_modules')}, indent=2))
    print('Exact JSON matches:', sum(c['exact_structural_match'] for c in comparisons), '/', len(comparisons))
    for record in comparisons:
        if record['differing_paths']:
            print(record['path'], record['differing_paths'])
    assert result.wasSuccessful(), stream.getvalue()
    return receipt


if __name__ == '__main__':
    run()
