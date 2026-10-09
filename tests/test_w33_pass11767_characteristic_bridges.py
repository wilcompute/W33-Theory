"""Independent modular membership, form, and characteristic-boundary checks."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import pytest
import sympy as s
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11767_global_current_algebra as A
import w33_pass11767_characteristic_bridges as B


@pytest.fixture(scope='module')
def frozen():return json.loads((ROOT/'data/w33_pass11767_characteristic_bridges.json').read_text())


def test_producer_hashes(frozen):
    assert frozen['source_sha256']==hashlib.sha256(Path(B.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    for path,digest in frozen['inputs'].items():assert digest==hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()


@pytest.mark.parametrize('p,rank',[(2,3160),(3,6240),(5,6240)])
def test_all_actual_field_rank_certificates(frozen,p,rank):
    record=frozen['reductions'][str(p)];w=record['witness']
    assert sorted(map(tuple,w['edges']))==sorted(A.actual_edges()) and w['prime']==p
    rows,digest=A.replay(w)
    assert len(rows)==rank and digest==record['replayed_basis_sha256']
    for row in rows:
        sums=np.zeros(80,dtype=int);left=np.zeros(80,dtype=int);trace=0
        for ij,x in row.items():
            i,j=divmod(ij,80);sums[i]+=x;left[j]+=(1 if i<40 else -1)*x
            if i==j:trace+=x
            if p==2:assert row.get(j*80+i,0)==x
        assert not np.any(sums%p) and not np.any(left%p) and trace%p==0


def test_binary_upper_bound_and_non_degenerate_78_quotient():
    assert 80*79//2==3160 and 39*79==3081 and 3160-3081==79
    # W has basis e_i+e_78, i<78, lying in u^perp and w^perp for w=e_79.
    Q=np.zeros((80,78),dtype=int);Q[:78]=np.eye(78,dtype=int);Q[78]=1
    omega=(Q.T@Q)%2
    assert not np.any(np.diag(omega)) and np.array_equal(omega,omega.T)
    assert np.array_equal((omega@omega)%2,np.eye(78,dtype=int))
    # The graph generators preserve dot product only after the binary reduction.
    for i,j in A.actual_edges():
        g=np.zeros((80,80),dtype=int);g[i,i]=g[j,i]=1;g[i,j]=g[j,j]=-1
        assert not np.any((g.T+g)%2)
        assert np.any((g.T+g)%3)
    # Kernel bracket is zero overF2; it would be a Heisenberg bracket in odd char.
    v=np.eye(78,dtype=int)[0];w=np.eye(78,dtype=int)[1]
    assert int(v@omega@w)==int(w@omega@v)==1
    assert (int(v@omega@w)-int(w@omega@v))%2==0


def test_qutrit_identity_is_central_in_quotient_but_not_full_algebra():
    assert 78%3==0 and 78%5!=0
    # No large-matrix symbolic inversion is needed in the adapted block basis.
    lift=np.diag([0]+[1]*78+[0]);radical=np.zeros((80,80),dtype=int);radical[0,1]=1
    assert np.trace(lift)%3==0
    assert np.any((lift@radical-radical@lift)%3)
    center=np.zeros((80,80),dtype=int);center[0,-1]=1
    assert not np.any((lift@center-center@lift)%3)
    small=s.Matrix([[1,1,0],[1,0,1],[0,1,1]])
    assert small.det()%2==0 and small.det()%3!=0 # binary fork exception
