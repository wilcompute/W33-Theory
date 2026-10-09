"""Actual global current generators in characteristics2,3,5, with rank replay.

This distinguishes binary/qutrit reductions of the same integer matrices;
it does not identify their quantum state spaces or import a modular Levi theorem.
"""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11767_global_current_algebra as A
OUT=ROOT/'data/w33_pass11767_characteristic_bridges.json'


def payload():
    records={}
    for p,target in ((2,3160),(3,6240),(5,6240)):
        w=A.rank_witness(A.actual_edges(),80,p,target);rows,digest=A.replay(w)
        assert len(rows)==target
        for row in rows:
            sums=[0]*80;left=[0]*80;trace=0
            for ij,x in row.items():
                i,j=divmod(ij,80);sums[i]+=x;left[j]+=(1 if i<40 else -1)*x
                if i==j:trace+=x
                if p==2:assert row.get(j*80+i,0)==x
            assert all(x%p==0 for x in sums+left+[trace])
        records[str(p)]=dict(rank=target,witness=w,replayed_basis_sha256=digest)
    return dict(schema='w33.pass11767.characteristics.v1',status='PASS',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        inputs={'analysis/w33_pass11767_global_current_algebra.py':hashlib.sha256(Path(A.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()},
        reductions=records,
        characteristic2_exact_space='All symmetric80x80 matrices A overF2 with A*ones=0; dimension80*79/2=3160. Trace zero follows automatically from symmetry and zero row sums.',
        characteristic2_upper_bound_proof='Off-diagonal symmetric entries are arbitrary; the80 row-sum equations uniquely determine the80 diagonal entries. The commutator of two symmetric matrices is symmetric in characteristic2. Thus the3160-row replay attains this invariant upper bound.',
        characteristic2_quotient='On W=u^perp/<u>, dim78, dot product descends to a nondegenerate alternating form, preserved by the current algebra. This is the exceptional binary configuration-form case; it does not contradict the characteristic-zero fork obstruction.',
        characteristic2_kernel='The action on W surjects onto sp(W), dimension3081, with an abelian79-dimensional kernel. In a basis (u,W,w), the kernel has A=[[0,v^T Omega,z],[0,0,v],[0,0,0]]. Its commutator vanishes because Omega is alternating and characteristic2. No characteristic-zero Heisenberg decomposition is asserted here.',
        odd_characteristic_exact_space='For p=3,5 the6240-dimensional space is A*u=0,s^T*A=0,tr(A)=0, with the same integral adapted block basis as overQ. Independent modular replay attains its6240 upper bound.',
        characteristic3_warning='The quotient block is sl78(F3), and78=0 inF3: I78 has trace zero and is central in that quotient block. Its lift diag(0,I78,0) acts nontrivially on the row/column radical. The full current algebra still has only the u*s^T center. A characteristic-zero semisimple Levi interpretation must not be copied toF3.',
        interpretation='These are exact reductions of one actual160-generator integer-current ansatz. Neither rank agreement nor the number3 supplies a qutrit Hilbert space, an E8 gauge identification or a gravity law.')


if __name__=='__main__':
    value=payload();OUT.write_text(json.dumps(value,separators=(',',':'))+'\n')
    print('11767 characteristic replay PASS: F2=3160, F3=6240, F5=6240',flush=True)
