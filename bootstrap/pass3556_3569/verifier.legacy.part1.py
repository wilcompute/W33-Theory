      'pairs_with_cap_four':candidate_434,
      'maximum_union_representative':{'columns':[bestrow[4],bestrow[5]],'direction_counts':bestrow[2],'zero_rows':bestrow[3],'cap':-bestrow[1]},
      'rank_three_heavy_pilot':{'selected_columns':64,'triples_exhausted':triple_count,'maximum_union_support':triple_max_union,'maximum_occupied_PG2_directions':triple_max_dirs,'maximum_direction_population':triple_max_pop,'cap_histogram':{str(k):v for k,v in sorted(triple_cap.items())},'best_columns':[triple_best[5],triple_best[6],triple_best[7]],'best_direction_counts':triple_best[3],'best_zero_rows':triple_best[4]},
      'method_boundary':'No one-circuit proof reaches 434; in this exact fundamental basis, the pure two-circuit direction-class pigeonhole method cannot prove 433, and 790 pairs remain possible 434 candidates requiring label-sensitive optimization.',
      'live_interval':[389,435]}

def block2(x,y):return sp.Matrix([[x,-y],[y,x-y]])

def amplitude_matrices(geo):
    a,b,c=geo['faces'][0];support={tuple(sorted((a,c))),tuple(sorted((b,c)))}
    mats=[sp.zeros(90) for _ in range(5)];counts=[0]*5
    for u,v in geo['graph_edges']:
        e=(u,v);ends={u,v}
        if e in support:ch=0;uv=(0,1);vu=(-1,-1)
        elif ends=={a,b}:ch=1;uv=vu=(1,0)
        elif c in ends:ch=2;uv=vu=(1,0)
        elif a in ends or b in ends:ch=3;uv=vu=(1,0)
        else:ch=4;uv=vu=(1,0)
        counts[ch]+=1
        mats[ch][2*u:2*u+2,2*v:2*v+2]=block2(*uv)
        mats[ch][2*v:2*v+2,2*u:2*u+2]=block2(*vu)
    assert counts==[2,1,30,60,627]
    return mats,counts

def amplitude_certificate(geo):
    mats,counts=amplitude_matrices(geo)
    C=mats[0].row_join(mats[1]).row_join(mats[2]).row_join(mats[3])
    B=sp.Matrix.hstack(*C.columnspace())
    while True:
        D=B.row_join(sp.Matrix.hstack(*(M*B for M in mats)))
        new=sp.Matrix.hstack(*D.columnspace())
        if new.shape[1]==B.shape[1]:break
        B=new
    assert B.shape==(90,14)
    _,piv=B.T.rref();rows=list(piv);Binv=B[rows,:].inv();restricted=[]
    for M in mats:
        X=Binv*(M*B)[rows,:];assert M*B==B*X;restricted.append(X)
    w=sp.symbols('w0:5');x=sp.symbols('x')
    A=sum((w[i]*restricted[i] for i in range(5)),sp.zeros(14))
    # The active real 14-space is two copies of a 7D rational characteristic factor.
    powA=sp.eye(14);powers=[]
    for k in range(1,8):
        powA=powA*A;powers.append(sp.expand(sp.trace(powA)/2))
    e=[sp.Integer(1)]
    for k in range(1,8):
        z=sum((-1)**(i-1)*e[k-i]*powers[i-1] for i in range(1,k+1));e.append(sp.cancel(z/k));assert sp.denom(e[-1])==1
    p=sp.factor(sum((-1)**k*e[k]*x**(7-k) for k in range(8)))
    fs=sp.factor_list(p)[1];q2=[f for f,n in fs if sp.Poly(f,x).degree()==2][0];q5=[f for f,n in fs if sp.Poly(f,x).degree()==5][0]
    expected_q2=x**2+(w[1]+w[4])*x+w[1]*w[4]-9*w[3]**2
    assert sp.expand(q2-expected_q2)==0
    # Exact scalar quotient.  The common kernel of the first four channels has
    # dimension 76 and is invariant under channel four.  Its action satisfies
    # (X+4I)(X-2I)=0 with trace -52, hence multiplicities 34 and 42 in the
    # real representation, i.e. 17 and 21 in the complex Hermitian spectrum.
    comp=[i for i in range(90) if i not in rows]
    # In the basis [B, e_j (j in comp)], the quotient action is the Schur coordinate block.
    X4=mats[4].extract(comp,comp)-B.extract(comp,range(14))*Binv*mats[4].extract(rows,comp)
    I76=sp.eye(76);assert (X4+4*I76)*(X4-2*I76)==sp.zeros(76) and sp.trace(X4)==-52
    # Exact dyadic witness.
    N=32768;nums=[-15576,44300,-28135,-30786,N]
    q=sp.Poly(sp.expand(p.subs(dict(zip(w,nums)))),x)
    lo=-4*N;hi=32*N
    assert q.count_roots(-sp.oo,lo)==0 and q.count_roots(lo,hi)==7 and q.count_roots(hi,sp.oo)==0
    ints=q.intervals(eps=sp.Rational(1,10**18));maxlo,maxhi=ints[-1][0]
    ratio_lo=sp.Rational(1)+maxlo/(4*N);ratio_hi=sp.Rational(1)+maxhi/(4*N)
    assert ratio_lo>sp.Rational(890622,100000) and ratio_hi<sp.Rational(890623,100000)
    fac=sp.factor(q.as_expr());faclist=[str(f) for f,n in sp.factor_list(q.as_expr())[1]]
    assert sorted(sp.Poly(f,x).degree() for f,n in sp.factor_list(q.as_expr())[1])==[2,5]
    # Exact double-boundary equations and algebraic KKT value polynomial.
    A2,B2,D2=sp.symbols('A B D')
    boundary=sp.expand(-15*A2**2*B2**2+16*A2**2*B2+16*A2*B2**2+A2*B2*D2-16*A2*B2+D2**2)
    P18=sp.Poly(93025*x**18-17368225*x**17+1343400488*x**16-54678836049*x**15+1208553186349*x**14-12568450299944*x**13+10408544953776*x**12+714023927292800*x**11-1918647323370496*x**10-9561946282978816*x**9+30508028220947456*x**8+46430249171922944*x**7-177191425380765696*x**6-90189547073110016*x**5+465447399548256256*x**4+53781503347261440*x**3-558321296207773696*x**2+9381546725212160*x+252166415161753600,x)
    klo=sp.Rational(790623,25000);khi=sp.Rational(3162493,100000)
    assert P18.count_roots(klo,khi)==1
    return {
      'channel_sizes':counts,'active_real_dimension':14,'rational_factor_degree':7,
      'global_characteristic_factorization':'(x+4 w4)^17 (x-2 w4)^21 q2(x)^2 q5(x)^2',
      'quadratic_factor':str(expected_q2),'quintic_factor':str(q5),
      'double_boundary_equations':['w1+3*w3^2=4','w0^2+w0*w2*w3+2*w1*w2^2-2*w1-9*w2^2*w3^2+8*w2^2+10*w3^2-8=0'],
      'dyadic_witness':{'denominator':N,'numerators':nums,'residual_factorization':str(fac),'ratio_lower':str(ratio_lo),'ratio_upper':str(ratio_hi),'certified_decimal_interval':['8.90622','8.90623']},
      'kkt_candidate':{'value_polynomial':str(P18.as_expr()),'root_interval':[str(klo),str(khi)],'approximate_value':31.624923044652377,'hoffman_ratio_approx':8.90623076116309,'status':'algebraic stationary candidate; global unrestricted optimality not certified'},
      'invariant_boundary_polynomial':str(boundary),
      'boundary':'The 2+5 factorization and dyadic witness are exact; the unrestricted real-cone optimum remains open.'
    }


def gf2_rank_rows(rows,bits):
    rows=rows[:];r=0
    for c in range(bits-1,-1,-1):
        p=next((i for i in range(r,len(rows)) if (rows[i]>>c)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(len(rows)):
            if i!=r and ((rows[i]>>c)&1):rows[i]^=rows[r]
        r+=1
    return r

def weight_enum(cols):
    h=collections.Counter()
    for m in range(32):h[sum(((m&c).bit_count()&1) for c in cols)]+=1
    return dict(sorted(h.items()))
def kraw(n,j,i):return sum((-1)**s*math.comb(i,s)*math.comb(n-i,j-s) for s in range(max(0,j-(n-i)),min(j,i)+1))
def dual_enum(n,A):
    out={}
    for j in range(n+1):
        z=sum(A.get(i,0)*kraw(n,j,i) for i in range(n+1));assert z%32==0
        if z//32:out[j]=z//32
    return out

def all_subspaces(r):
