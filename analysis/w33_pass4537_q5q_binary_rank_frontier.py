#!/usr/bin/env python3
"""Pass 4537 -- Q(5,q) binary-rank law frontier with an independent q=7 anchor.

Pass 4530 reduced the protected apartment quotient for Q(5,q)=GQ(q,q^2),
q=3 mod 4, to rho(q)=rank_2(N^T N), but did not know a closed formula.
This pass constructs the elliptic quadric Q^-(5,q) directly over prime fields
q=3 and q=7, enumerates all totally singular lines, and computes exact binary
ranks using integer bitset elimination.

Results:
  q=3: rank N=91, rank(N^T N)=70;
  q=7: rank N=2451, rank(N^T N)=2150.
Both satisfy
  dim ker(N^T)=q(q^2-q+1),
  rho(q)=(q^2+1)(q^2-q+1)=#lines/(q+1).
For every odd-q GQ(q,q^2), the line graph has even SRG parameters k,lambda,mu,
so its binary adjacency A=N^T N obeys A^2=0.  This supplies the general upper
bound rho <= #lines/2 but not the conjectured equality/formula.

The all-q formula is therefore recorded as a conjecture, not a theorem.  The
q=7 computation is independent of the repository's Q(5,3) builder and is small
enough to be rerun as an exact regression witness.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4537_Q5Q_BINARY_RANK_FRONTIER.json'


def rank_bits(rows):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)


def nonsquare(q):
    return next(a for a in range(2,q) if pow(a,(q-1)//2,q)==q-1)


def build_qminus(q:int):
    d=nonsquare(q)
    pts=[]
    for lead in range(6):
        for tail in itertools.product(range(q),repeat=5-lead):
            x=(0,)*lead+(1,)+tail
            if (x[0]*x[0]-d*x[1]*x[1]+x[2]*x[3]+x[4]*x[5])%q==0:
                pts.append(x)
    pidx={p:i for i,p in enumerate(pts)}
    def norm(v):
        for z in v:
            if z%q:
                inv=pow(z%q,-1,q)
                return tuple((inv*(a%q))%q for a in v)
        raise ValueError('zero projective vector')
    def B(x,y):
        return (2*x[0]*y[0]-2*d*x[1]*y[1]+x[2]*y[3]+x[3]*y[2]+x[4]*y[5]+x[5]*y[4])%q
    lines=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if B(x,y):continue
            S=set()
            for a,b in itertools.product(range(q),repeat=2):
                if a or b:
                    S.add(pidx[norm(tuple((a*x[k]+b*y[k])%q for k in range(6)))])
            assert len(S)==q+1
            lines.add(tuple(sorted(S)))
    return pts,sorted(lines),d


def exact_ranks(q):
    pts,lines,d=build_qminus(q)
    P=(q+1)*(q**3+1); L=(q**2+1)*(q**3+1)
    assert (len(pts),len(lines))==(P,L)
    point_lines=[[] for _ in pts]; line_masks=[]
    for li,line in enumerate(lines):
        m=0
        for p in line:
            m|=1<<p;point_lines[p].append(li)
        line_masks.append(m)
    rankN=rank_bits(line_masks)
    adj=[]
    for li,line in enumerate(lines):
        m=0
        for p in line:
            for lj in point_lines[p]:m|=1<<lj
        m^=1<<li
        assert m.bit_count()==q**2*(q+1)
        adj.append(m)
    rankA=rank_bits(adj)
    return {'q':q,'nonsquare_d':d,'points':P,'lines':L,'rank_N':rankN,
            'ker_Nt_dimension':P-rankN,'rank_NtN':rankA,
            'candidate_rho_formula':(q*q+1)*(q*q-q+1),
            'candidate_kernel_formula':q*(q*q-q+1)}


def main():
    rows=[exact_ranks(3),exact_ranks(7)]
    assert [(r['rank_N'],r['rank_NtN']) for r in rows]==[(91,70),(2451,2150)]
    assert all(r['rank_NtN']==r['candidate_rho_formula'] for r in rows)
    assert all(r['ker_Nt_dimension']==r['candidate_kernel_formula'] for r in rows)

    # General odd-q SRG parity theorem. For GQ(q,q^2) line graph:
    # k=q^2(q+1), lambda=q^2-1, mu=q+1. All are even when q is odd.
    # A^2=(k-mu)I+(lambda-mu)A+mu J reduces to zero over F2.
    symbolic={
      'line_graph_parameters':{'k':'q^2(q+1)','lambda':'q^2-1','mu':'q+1'},
      'odd_q_parities':'k=lambda=mu=0 mod 2',
      'consequence':'A^2=0 over F2, hence im(A) <= ker(A) and rank_2(A) <= number_of_lines/2'
    }
    out={
      'pass':4537,
      'exact_prime_field_anchors':rows,
      'general_odd_q_square_zero_theorem':symbolic,
      'closed_rank_conjecture':'rank_2(N^T N)=(q^2+1)(q^2-q+1)=#lines/(q+1) for odd q; for q=3 mod4 this is the Pass-4530 protected apartment dimension',
      'companion_incidence_conjecture':'dim ker(N^T)=q(q^2-q+1), equivalently rank N=(q+1)(q^3+1)-q(q^2-q+1)',
      'status':'EXACT at q=3 and q=7; general A^2=0 theorem exact; closed rank formula remains unproved',
      'theorem':'An independent Q^-(5,7) construction gives rank N=2451 and rank(N^T N)=2150, exactly matching the closed candidate law; the all-odd-q adjacency is square-zero over F2.',
      'boundary':'Do not promote the two-anchor rank formula to an all-q theorem without a modular-representation/code proof. Published incidence-rank tables are external corroboration, not encoded as proof in this executable.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
