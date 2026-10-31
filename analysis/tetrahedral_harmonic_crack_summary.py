import json
from statistics import mean, median


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def summarize_heawood_fano_alignment(path='heawood_fano7_tetra_alignment.json'):
    data = load_json(path)
    examples = data.get('examples', [])

    op_diffs = [e['op_diff'] for e in examples if 'op_diff' in e]
    lap_diffs = [e['lap_diff'] for e in examples if 'lap_diff' in e]
    comm_norms = [e['comm_norm'] for e in examples if 'comm_norm' in e]
    subspace_resids = [e['subspace_resid'] for e in examples if 'subspace_resid' in e]

    return {
        'graph_nodes': data.get('heawood_graph_nodes'),
        'graph_edges': data.get('heawood_graph_edges'),
        'fano_7cycles': data.get('fano_7cycles'),
        'tetra_op_shape': data.get('tetra_operator_shape'),
        'op_diff_mean': mean(op_diffs) if op_diffs else None,
        'op_diff_median': median(op_diffs) if op_diffs else None,
        'lap_diff_max': max(lap_diffs) if lap_diffs else None,
        'comm_norm_mean': mean(comm_norms) if comm_norms else None,
        'subspace_resid_mean': mean(subspace_resids) if subspace_resids else None,
        'op_diff_values_sample': op_diffs[:5],
        'subspace_resid_sample': subspace_resids[:5],
    }


def summarize_heawood_tetra_oscillator(path='heawood_tetra_oscillator.json'):
    data = load_json(path)
    return {
        'laplacian_eigenvalues': data.get('laplacian_eigenvalues'),
        'tetra_operator_eigenvalues': data.get('tetra_operator_eigenvalues'),
        'cluster_labels': data.get('cluster_labels'),
    }


import math

def summarize_natural_constants():
    phi = (1 + math.sqrt(5)) / 2
    sqrt2 = math.sqrt(2)
    e = math.e
    pi = math.pi

    heawood = summarize_heawood_tetra_oscillator()['laplacian_eigenvalues']
    if heawood is None or len(heawood) < 2:
        return {'error': 'no heawood eigenvalues available'}

    # use the first non-zero eigenvalue and first high-value for comparison
    lam1 = float(heawood[1])
    lam2 = float(heawood[-1])
    ratio = lam2 / lam1 if lam1 != 0 else None

    # closeness to golden ratio and other constants
    def closeness(val, target):
        return abs(val - target)

    return {
        'phi': phi,
        'sqrt2': sqrt2,
        'pi': pi,
        'e': e,
        'heawood_lambda1': lam1,
        'heawood_lambdan': lam2,
        'heawood_ratio': ratio,
        'heawood_vs_phi_diff': closeness(ratio, phi) if ratio is not None else None,
        'heawood_vs_sqrt2_diff': closeness(ratio, sqrt2) if ratio is not None else None,
        'heawood_vs_pi_diff': closeness(ratio, pi) if ratio is not None else None,
        'heawood_vs_e_diff': closeness(ratio, e) if ratio is not None else None,
    }


def summarize_tetrahedral_harmonic_comparison(path='tetrahedral_harmonic_comparison.json'):
    data = load_json(path)
    return {
        'tetra_laplacian_gap': data['comparison'].get('tetra_laplacian_gap'),
        'heawood_laplacian_gap': data['comparison'].get('heawood_laplacian_gap'),
        'gap_ratio': data['comparison'].get('gap_ratio'),
    }


def main():
    out = {
        'heawood_fano_alignment': summarize_heawood_fano_alignment(),
        'heawood_tetra_oscillator': summarize_heawood_tetra_oscillator(),
        'tetrahedral_harmonic_comparison': summarize_tetrahedral_harmonic_comparison(),
        'natural_constants_alignment': summarize_natural_constants(),
    }

    with open('tetrahedral_harmonic_crack_summary.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

    print('Wrote tetrahedral_harmonic_crack_summary.json')
    print('Summary:', out['heawood_fano_alignment'])


if __name__ == '__main__':
    main()
