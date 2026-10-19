"""Explicit invertible COMPLEX 27x27 Peirce-coordinate map from first
Tits J(M3(C),1) to 3 singlets + three 8D quadratic-norm octets.
This is a necessary step to the canonical Cayley-Dickson J3(O_C)
map; trilinear tensors still require independent triality rotations.
"""
import json,itertools
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round12_peirce_27_map.json"
def decode(v):
    A=S.Matrix(3,3,v[:9]);B=S.Matrix(3,3,v[9:18]);C=S.Matrix(3,3,v[18:])
    return A,B,C
def N(v):
    A,B,C=decode(v)
    return A.det()+B.det()+C.det()-S.trace(A*B*C)
def basisvector(i):
    x=S.zeros(27,1);x[i]=1;return x
def index(mat,row,col):return mat*9+3*row+col
def run():
    # Define three offdiagonal octets V_ij=(A_ij,A_ji,
    #  B_k0,B_k1,B_k2,C_0k,C_1k,C_2k), for k distinct from i,j.
    # Each octet comes in 4 conjugate hyperbolic pairs.
    M=S.zeros(27)
    # source coordinates (27) = first Tits block A[9], B[9], C[9].
    # target coordinates 0,1,2 are diagonal singlets.
    for i in range(3): M[index(0,i,i),i]=1
    octets=[(0,1,2),(1,2,0),(2,0,1)]
    sources=[]
    for g,(i,j,k) in enumerate(octets):
        pairs=[(index(0,i,j),index(0,j,i))]
        pairs += [(index(1,k,l),index(2,l,k)) for l in range(3)]
        sources.append(pairs)
        for h,(left,right) in enumerate(pairs):
            # v_{2h}^2+v_{2h+1}^2 = source[left]*source[right].
            # Each source hyperbolic pair has coefficient 1 for v0²,v1².
            t=3+8*g+2*h
            M[left,t]=1; M[right,t]=1
            M[left,t+1]=S.I; M[right,t+1]=-S.I
    assert M.rank()==27
    assert M.det()!=0
    t=S.symbols("a0:3")
    tests=[]
    for k in range(3):
      for g,(i,j,compl) in enumerate(octets):
        for m in range(8):
            col=3+8*g+m
            vec=sum((t[l]*M[:,l] for l in range(3)),S.zeros(27,1))+M[:,col]
            n=S.expand(N(vec))
            baseline=t[0]*t[1]*t[2]
            if k==compl:
                assert S.expand(n-baseline+t[k])==0
    # Build *exact* entire cubic in target octet basis via evaluations:
    # det(sum a_i Ei + sum x U + sum y V + sum z W)
    # = abc - a norm(O_12) - b norm(O_20) - c norm(O_01)
    #     + octet cross trilinear.
    # With our octets V01,V12,V20: complementary diag respectively 2,0,1.
    tri={}
    for i,j,k in itertools.product(range(8),repeat=3):
        x=M[:,3+i]+M[:,11+j]+M[:,19+k]
        z=S.simplify(N(x))
        if z!=0:
            tri[f"{i},{j},{k}"]=str(z)
    singlet_oct_quadratic=[]
    for g,(i,j,k) in enumerate(octets):
        for m in range(8):
            x=M[:,k]+M[:,3+8*g+m]
            singlet_oct_quadratic.append(str(N(x)))
    assert all(v=="-1" for v in singlet_oct_quadratic)
    # For canonical Cayley-Dickson normalization, the 64 nonzero
    # trilinear basis coefficients all have abs=2; classify difference
    # and whether this frame already matches it up to simple relabeling.
    vals=[S.simplify(v) for v in tri.values()]
    hist={}
    for v in vals:
        name=str(S.simplify(v));hist[name]=hist.get(name,0)+1
    checks={"full_27x27_complex_isomorphism_of_vector_spaces":M.rank()==27,
       "three_Peirce_octets_8_each":len(sources)==3 and all(len(x)==4 for x in sources),
       "diagonal_singlets_cubic":N(M[:,0]+M[:,1]+M[:,2])==1,
       "all_24_octet_norm_coefficients_exact_minus_one":all(v=="-1" for v in singlet_oct_quadratic),
       "cross_tensor_is_nonzero":len(tri)>0}
    out={"schema":"w33.round12.Peirce_27x27_complex_coordinate_map.v1",
      "description":"Explicit 27x27 full-rank complex-linear transformation from first Tits 27 coordinates into 3 diagonal singlets plus 3 Peirce offdiagonal 8-planes, where every octet norm is sum of eight complex squares and all diagonal-octet cubic terms match the standard Jordan pattern. NONTRIVIAL offdiagonal basis mixing uses (x+i y, x-i y) in each of four hyperbolic source pairs. This is not yet an E6 intertwiner to the CANONICAL Cayley-Dickson octonion multiplication; check its cross-octet tensor and solve remaining SO8^3 triality changes.",
      "map_columns_firstTits_coordinates_rows_to_3plus8plus8plus8": [[str(x) for x in row] for row in M.tolist()],
      "complex_determinant":str(M.det()),"cross_octet_nonzero_monomials":len(tri),
      "cross_octet_coefficient_histogram":hist,
      "cross_octet_sparse_tensor":tri,"source_hyperbolic_pairs":sources,
      "checks":checks,"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"det":out["complex_determinant"],"cross":len(tri),"hist":hist},indent=2))
    return out
if __name__=="__main__":run()
