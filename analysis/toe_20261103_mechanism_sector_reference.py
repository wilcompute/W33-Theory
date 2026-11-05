"""Connect the new4D flux index to the repo's existing Kato frame machinery.

Different positive-projector ranks prohibit a common everywhere-gapped path.
The old heavy optical frame remains valid; it is not an acoustic-sector proof.
"""
import json,itertools,pathlib
import numpy as np
from toe_20261103_mechanism_four_dimensional_overlap import links,gammas
ROOT=pathlib.Path(__file__).resolve().parents[1]

def kernel(U,L):
    # Assemble independently as shift matrices, rather than reusing the old
    # site-block Wilson loop. Site-major tensor ordering matches that producer.
    gs,g5=gammas();xs=list(itertools.product(range(L),repeat=4));ix={x:i for i,x in enumerate(xs)};n=len(xs)
    A=3*np.eye(4*n,dtype=complex)
    for mu in range(4):
        T=np.zeros((n,n),complex)
        for i,x in enumerate(xs):
            y=list(x);y[mu]=(y[mu]+1)%L;T[i,ix[tuple(y)]]=U[i,mu]
        A-=.5*(np.kron(T,np.eye(4)-gs[mu])+np.kron(T.conj().T,np.eye(4)+gs[mu]))
    return np.kron(np.eye(n),g5)@A

def build():
    L=3;A=kernel(links(L,0,0),L);B=kernel(links(L,1,1),L)
    ea,va=np.linalg.eigh(A);eb,vb=np.linalg.eigh(B)
    E=va[:,ea>0];T=vb[:,eb>0];P=T@T.conj().T
    n0,n1=E.shape[1],T.shape[1];assert(n0,n1)==(162,163)
    projected=P@E;u,z,_=np.linalg.svd(projected,full_matrices=False);rank=int(sum(z>1e-9))
    F=u[:,:rank];missing=P-F@F.conj().T
    deficiency=n1-rank;norm=float(np.linalg.norm(missing,2));assert deficiency>=1 and norm>1-1e-10
    # Any continuous gapped Hermitian path would have constant positive rank.
    # A concrete affine path brackets one gap closure; intermediate matrices
    # are Hermitian comparison operators, NOT necessarily Wilson gauge kernels.
    lo,hi=0.,1.;records=[]
    for _ in range(28):
        t=(lo+hi)/2;e=np.linalg.eigvalsh((1-t)*A+t*B);n=int(sum(e>0))
        records.append(dict(t=t,positive_rank=n,min_absolute_eigenvalue=float(min(abs(e)))))
        if n==n0:lo=t
        else:hi=t
    near=(lo+hi)/2;e=np.linalg.eigvalsh((1-near)*A+near*B);gap=float(min(abs(e)))
    assert gap<1e-6
    return dict(status='PASS_FLUX_SECTOR_REFERENCE_RANK_OBSTRUCTION',L=L,
        free_positive_projector_rank=n0,flux_positive_projector_rank=n1,
        free_index=int(-np.sum(np.sign(ea))/2),flux_index=int(-np.sum(np.sign(eb))/2),
        endpoint_kernel_gaps=[float(min(abs(ea))),float(min(abs(eb)))],
        projected_free_reference_rank=rank,missing_target_dimensions=deficiency,endpoint_frame_projector_operator_error=norm,
        affine_gap_closure_bracket=[lo,hi],near_crossing_gap=gap,bisection_records=records,
        theorem='For a continuous Hermitian family on one fixed finite Hilbert space with no zero eigenvalue, the positive spectral projector has constant integer rank. These endpoints have162 and163. Therefore EVERY such interpolating family has a zero eigenvalue somewhere. This rank theorem is standard; the endpoints and deficient reference map are actual matrices of the new4D flux regulator.',
        frame_failure='A162-column free reference E cannot span the163-dimensional target chiral subspace. Polar normalization of Ptarget E cannot create the missing column. The operator norm of the resulting projector error is1. This is a dimension obstruction, not a small discretization error.',
        prior_owner='analysis/w33_pass12002_native_path_overlap.py constructs an onsite-reference Kato frame for uniformly positive-mass HEAVY optical blocks. That proof remains valid. It does not trivialize an acoustic block of different index. Pass12030 already owns a distinct toron Chern/sector-frame obstruction; Pass12038 owns finite non-Abelian patch transitions; Oct27 acoustic-density code already implements a finite projector comparison current.',
        implication='A measure construction needs compatible reference data for each index component (and suitable insertions/rectangular Weyl maps), followed by locality and global-integrability checks within components. Failure to connect two different-index sectors by a gapped path is expected and does NOT disprove the Craig/Luscher measure constructions or the physical existence of chiral gauge theory.',
        limits='Finite numeric endpoint spectral gaps and a numerical affine crossing bracket, not interval-certified eigenvalues or a new general theorem. No all-volume locality, admissibility matching, full Weyl measure, unique inter-component phase or interacting continuum model is established.',
        sources=['https://arxiv.org/html/2610.09093v1#S4.SS3','https://arxiv.org/html/2610.09093v1#S5','https://arxiv.org/abs/hep-lat/9811032'])

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_mechanism_sector_reference.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['missing_target_dimensions'],d['near_crossing_gap'],flush=True)
