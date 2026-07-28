#!/usr/bin/env python3
"""
Pass 1245: species-20 matrix-unit GAP manifest.

Creates the concrete GAP manifest listing the exact ingredients and command
sequence required to materialize the species-20 matrix units.
"""
import json
from pathlib import Path
from datetime import datetime


def main():
    gap_manifest = {
        'session_preamble': [
            'LoadPackage("atlasrep");',
            'LoadPackage("ctbllib");',
            'LoadPackage("meataxe");'
        ],
        'objects_to_load': [
            'W(E6) character table',
            'Degree-20 irreducible matrix representation of W(E6)',
            'Residual central projector P_20 from data/w33_pass1194_residual_central_idempotents.json',
            'Ambient 1952-dim residual action matrices'
        ],
        'command_sequence': [
            'Construct the ambient residual module R of dimension 1952.',
            'Load or reconstruct the species-20 central projector P20 in End(R).',
            'Compute Image(P20) and choose a nonzero seed vector v1.',
            'Generate a basis of the first 20-dim copy using the degree-20 representation action.',
            'Orthogonalize and search for additional copies if multiplicity > 1.',
            'Define e_ij^(ab) = v_i^(a) tensor dual(v_j^(b)).',
            'Verify e_ij^(ab) * e_kl^(cd) = delta_{bc} delta_{jk} e_il^(ad).',
            'Export each matrix unit to JSON or sparse-matrix text format.'
        ],
        'artifacts_expected': [
            'species20_basis_vectors.json',
            'species20_matrix_units.json',
            'species20_verification_report.json'
        ]
    }
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1245.species20_matrix_unit_gap_manifest.v1',
        'status': 'PASS',
        'species': 20,
        'commutant_block': 'M_20(Q)',
        'gap_manifest': gap_manifest,
        'goal': 'Materialize the first explicit commutant block with full matrix units in the residual 1952 module.'
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/w33_pass1245_species20_matrix_unit_gap_manifest.json').write_text(json.dumps(result, indent=2))
    print('PASS 1245 complete: species-20 matrix-unit GAP manifest written')
    return result

if __name__ == '__main__':
    main()
