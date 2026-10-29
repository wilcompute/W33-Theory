"""Exact symplectic doily polarity and involution verification."""
from analysis.w33_20261029_doily_polarity_twistor_involution import certificate,matrix,pairing


def test_polarity_symmetric_orthogonal():
    M,B=matrix()
    assert all(M[i][i]==1 for i in range(15))
    assert all(sum(M[i])==7 for i in range(15))
    assert all(sum(B[i][k]*B[k][j] for k in range(15)) == 36*(i==j)
               for i in range(15) for j in range(15))


def test_doily_srg_and_twistor_involution():
    c=certificate()
    assert c['point_collinearity_srg']==[15,6,1,3]
    assert c['T_eigenspaces']=={'+1':10,'-1':5}
    assert c['T_trace']==5
