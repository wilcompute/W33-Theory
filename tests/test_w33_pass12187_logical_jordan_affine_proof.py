from pathlib import Path
import itertools
import json
import hashlib
import sys
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12187_logical_jordan_affine_proof as m

@pytest.fixture(scope='module')
def cert():
    return json.loads((ROOT/'data/w33_pass12187_logical_jordan_affine_proof.json').read_text())

def test_certificate_source_and_scope(cert):
    assert cert['source_sha256']==hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()
    assert all(value is False for value in cert['scope'].values())
    assert cert['symbolic_zero_residuals']==m.symbolic_identities()

@pytest.mark.parametrize('p',[2,3,5])
def test_native_shortening_and_dual_projection(p,cert):
    assert m.projective_projection_control(p)==next(r for r in cert['projection_controls'] if r['p']==p)

@pytest.mark.parametrize('p',[2,3,5])
def test_actual_function_differences_and_intersections(p,cert):
    assert m.affine_matrix_control(p)==next(r for r in cert['affine_controls'] if r['p']==p)

@pytest.mark.parametrize('p',[2,3,5,7])
def test_binomial_difference_with_wraparound(p):
    # t=p-1 wraps to0; characteristic-p identity must still hold there.
    for t,i in itertools.product(range(p),repeat=2):
        diff=(m.binomial_value((t+1)%p,i,p)-m.binomial_value(t,i,p))%p
        expected=m.binomial_value(t,i-1,p) if i else 0
        assert diff==expected

@pytest.mark.parametrize('p',[2,3,5])
def test_against_independent_full_projective_quotient(p):
    row=m.prior.census(p)
    assert row['rank_powers_T_minus_I_on_Q']==[m.rank_formula(p,k) for k in range(p+1)]

def test_all_prime_rows_from_actual_integer_basis_counts(cert):
    for row in cert['prime_rows']:
        p=row['p']; ranks=row['ranks']
        assert ranks[0]==(p+1)*(p*p+1)-2*m.comb(p+2,3)
        assert ranks[-1]==0
        for k in range(1,p+1):
            image,intersection=m.affine_count(p,k)
            assert image-intersection==ranks[k]==m.rank_formula(p,k)
        blocks={int(j):v for j,v in row['blocks'].items()}
        assert blocks==m.prior.predicted_blocks(p)
        assert sum(blocks.values())==p*p+1
        assert sum(j*v for j,v in blocks.items())==ranks[0]

def test_prime_power_is_not_silently_substituted():
    with pytest.raises(AssertionError):m.rank_formula(9,1)
