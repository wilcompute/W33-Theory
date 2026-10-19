"""Explicit 40 D5 root ladder operators + 5 Cartans on 27=1+10+16,
via 5 complex fermionic creation/annihilation modes; transport by the
Round12 27x27 Tits-octonion map. Test E6 cubic compatibility honestly.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round14_so10_chevalley_transport.json"
def run():
    I=S.eye(32);a=[];ad=[]
    for j in range(5):
        A=S.zeros(32)
        for m in range(32):
            if (m>>j)&1:A[m^(1<<j),m]=(-1)**((m&((1<<j)-1)).bit_count())
        a.append(A);ad.append(A.T)
    assert all(a[i]*ad[j]+ad[j]*a[i]==(I if i==j else S.zeros(32)) for i in range(5) for j in range(5))
    even=[m for m in range(32) if m.bit_count()%2==0]
    spin=lambda X:X.extract(even,even)
    E=[];H=[];names=[];roots=[]
    for i in range(5):
        h=ad[i]*a[i]-I/2
        hv=S.zeros(10);hv[i,i]=1;hv[i+5,i+5]=-1
        H.append((hv,spin(h)))
    for i,j in itertools.permutations(range(5),2):
        v=S.zeros(10);v[i,j]=1;v[j+5,i+5]=-1
        E.append((v,spin(ad[i]*a[j])))
        names.append(f"e{i}-e{j}");roots.append(tuple(int(z==i)-int(z==j) for z in range(5)))
    for i,j in itertools.combinations(range(5),2):
        v=S.zeros(10);v[i,j+5]=1;v[j,i+5]=-1
        E.append((v,spin(ad[i]*ad[j])))
        names.append(f"e{i}+e{j}");roots.append(tuple(int(z==i)+int(z==j) for z in range(5)))
        v=S.zeros(10);v[i+5,j]=-1;v[j+5,i]=1
        E.append((v,spin(a[j]*a[i])))
        names.append(f"-e{i}-e{j}");roots.append(tuple(-int(z==i)-int(z==j) for z in range(5)))
    assert len(E)==40 and len(set(roots))==40
    for (v,b),r in zip(E,roots):
        assert all(hv*v-v*hv==r[k]*v and hs*b-b*hs==r[k]*b for k,(hv,hs) in enumerate(H))
    for i,j in itertools.combinations(range(5),2):
        pi=names.index(f"e{i}-e{j}");pj=names.index(f"e{j}-e{i}")
        ci=names.index(f"e{i}+e{j}");cj=names.index(f"-e{i}-e{j}")
        for t in (0,1):
            assert E[pi][t]*E[pj][t]-E[pj][t]*E[pi][t]==H[i][t]-H[j][t]
            assert E[ci][t]*E[cj][t]-E[cj][t]*E[ci][t]==H[i][t]+H[j][t]
    old=json.loads((ROOT/"data/w33_20261019_round12_full_octonion_intertwiner.json").read_text())
    T=S.Matrix([[S.sympify(x) for x in row] for row in old["target_to_firstTits_27x27"]])
    tab=json.loads((ROOT/"data/w33_20261019_round13_so10_transport.json").read_text())["clock_sectors"][0]
    vec=tab["ten_indices"];spi=tab["sixteen_indices"];one=tab["one_indices"];assert len(vec)==10 and len(spi)==16
    def embed(pair):
        B=S.zeros(27)
        for arr,idx in zip(pair,(vec,spi)):
            for i,j in itertools.product(range(len(idx)),repeat=2):
                if arr[i,j]:B[idx[i],idx[j]]=arr[i,j]
        return B
    ec=[embed(q) for q in E];hc=[embed(q) for q in H]
    Ti=T.inv()
    mapped=[T*B*Ti for B in ec]
    charge=S.diag(*[4 if j in one else -2 if j in vec else 1 for j in range(27)])
    assert all(charge*B==B*charge for B in ec)
    # The naive independent Fock label ordering has no reason to
    # preserve the E6 Jordan cubic, even though abstract SO10
    # representation and root relations are exact. Quantify this.
    from w33_20261019_round9_triality_cubic_texture import omul
    # cubic in first Tits coordinates, transformed root generator
    def norm(z):
        A=S.Matrix(3,3,z[:9]);B=S.Matrix(3,3,z[9:18]);C=S.Matrix(3,3,z[18:])
        return A.det()+B.det()+C.det()-S.trace(A*B*C)
    tests=[S.Matrix([((i*i+3*i+7*t)%11)-5 for i in range(27)]) for t in range(3)]
    mismatch=[]
    for g in mapped[:4]:
        valid=True
        for x in tests:
            y=g*x
            t=S.symbols("t")
            if S.expand(norm(x+t*y)).coeff(t,1)!=0:valid=False;break
        mismatch.append(not valid)
    checks={"40_exact_D5_roots":len(E)==40,
       "5_exact_D5_Cartan_generators":len(H)==5,
       "CAR_creation_annihilation_5modes":True,
       "all_40_weight_root_commutators_exact":True,
       "all_20_opposite_root_Chevalley_commutators_exact":True,
       "full_27x27_gaussian_integer_transport":all(g.shape==(27,27) for g in mapped),
       "all_40_commute_with_U1":True}
    out={"schema":"w33.round14.D5_fock_40root_27dim_transport.v1",
        "construction":"Five CAR fermion modes on Fock(32); even-parity spinor space dim16. SO10 generators 20 E_ei-ej=a_i†a_j (i!=j), ten pair creation E_ei+ej=a_i†a_j†, ten annihilation E_-ei-ej=a_j a_i. Vector rep W⊕W* dim10 from CAR commutators, spinor16 from even Fock. Block diagonal plus singlet 1 yields 27 representation. Conjugate all 40 roots via Round12 Tits-octonion invertible matrix. All root weight commutators and opposite Chevalley commutators checked exactly.",
        "root_labels":names,"roots_D5_integer_5tuple":[list(x) for x in roots],
        "transported_root_generators_27x27_sparse":[[(int(i),int(j),str(mapped[k][i,j])) for i,j in itertools.product(range(27),repeat=2) if mapped[k][i,j]] for k in range(40)],
        "first_four_naively_embedded_generators_fail_E6_cubic_lie_invariance":mismatch,
        "scope":"These are EXACT abstract D5=so10 representation generators transported through Albert COORDINATES. Their arbitrary chosen 10-vector and 16-spinor bases have NOT been matched to the specific octonionic cubic invariance, and may FAIL dN(Xx)=0; so they are NOT proven as the Pass12076 D5 LIE SUBALGEBRA OF E6. Finding the blockwise triality-compatible basis to match the cubic remains open. A direct group intertwiner from 120 Pauli ticks to 120 E8 clocks remains PROVED impossible (Pass12072).",
        "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"Nroots":len(E),"fail_cubic_first4":mismatch}))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
