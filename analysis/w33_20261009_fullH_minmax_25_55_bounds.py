"""Exact min-max eigenvalue COUNT certificates from independent
trivial, 24, 15p, 15l PSp(4,3) trial representations.

Distinct representation types are orthogonal in L2, and on the
lambda=-4 component the point/line incidence N vanishes, giving
mutually orthogonal 15-dim subspaces. The 24-dimensional 2/4/6 trial
ray transforms covariantly and has identical Rayleigh energy for each
of 24 orthonormal representation coordinates.
Hence at least 25 genuine eigenvalues <= max(E_trivial,E_24trial),
and 55 <= max(E_trivial,E_24,E_15p,E_15l).
This is an UPPER bound for ordered spectrum, not lower bound or
ground representation determination.
"""
from pathlib import Path
import sys,json
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
def certificate():
    source=json.loads((ROOT/'data/w33_20261009_he246_symmetry_exact_wick.json').read_text())
    wit=source['sectors']
    u24=F(wit['24']['rigorous_sector_lowest_energy_upper_endpoint'])
    up=F(wit['15_p']['rigorous_sector_lowest_energy_upper_endpoint'])
    ul=F(wit['15_l']['rigorous_sector_lowest_energy_upper_endpoint'])
    # certified 11-state trivial witness earlier proved E0<127.595507
    trivial=F('127.595507')
    bound25=max(trivial,u24)
    bound55=max(bound25,up,ul)
    assert bound25<F('142.435') and bound55<F('143.464')
    return dict(status='PASS',
       full_H_minmax_25th_eigenvalue_upper=str(bound25),
       full_H_minmax_55th_eigenvalue_upper=str(bound55),
       guaranteed_number_of_actual_eigenvalues_below_142_435=25,
       guaranteed_number_of_actual_eigenvalues_below_143_464=55,
       counting='Eigenvalues ordered including multiplicity (starting at index1). Single trivial Gaussian/Wick trial, 24 line-point isotypic trial copies, 15 point +15 line symmetry-orthogonal copies.',
       scalar_trivial_upper='127.595507',
       nontrivial_irreps={'24':str(u24),'15_p':str(up),'15_l':str(ul)},
       representation_proof='The strongly regular W33 point and line modules have 1+24+15. Hamiltonian is PSp-equivariant. The trivial one-state trial is orthogonal to 24 and both 15 types; 15 point/line cross Gram=0 since line-point incidence has zero singular value on 15. On 24, a fixed normalized multiplicity-space Hermite witness induces 24 orthonormal equivalent trial vectors. Thus min-max provides an upper bound on E_25 and E_55 of actual full H.',
       caution='This is NOT a bound from below, not proof of the true ground irrep/ground degeneracy, not a numerical physical gap, and not a claim that the Ritz trial eigenvalues equal full H eigenvalues.')
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261009_fullH_minmax_25_55_bounds.json').write_text(json.dumps(d,indent=2)+'\n')
    print('MINMAX',d['full_H_minmax_25th_eigenvalue_upper'],d['full_H_minmax_55th_eigenvalue_upper'])
