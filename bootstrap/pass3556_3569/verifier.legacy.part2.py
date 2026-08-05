    if r==0:return [{0}]
    seen=set();out=[]
    for tup in itertools.combinations(range(1,32),r):
        if gf2_rank_rows(list(tup),5)!=r:continue
        span={0}
        for z in tup:span|={y^z for y in list(span)}
        key=tuple(sorted(span))
        if key not in seen:seen.add(key);out.append(span)
    return out
SUB={r:all_subspaces(r) for r in range(1,6)}

@njit
def mapv(x,a,b,c,d,e):
    y=0
    if x&1:y^=a
    if x&2:y^=b
    if x&4:y^=c
    if x&8:y^=d
    if x&16:y^=e
    return y
@njit
def stabilizer_orders(masks,points,lens):
    nc=len(masks);counts=np.zeros(nc,np.int64)
    for a in range(1,32):
      span1=np.zeros(32,np.uint8);span1[0]=1;span1[a]=1
      for b in range(1,32):
       if span1[b]:continue
       span2=span1.copy()
       for z in range(32):
        if span1[z]:span2[z^b]=1
       for c in range(1,32):
        if span2[c]:continue
        span3=span2.copy()
        for z in range(32):
         if span2[z]:span3[z^c]=1
        for d in range(1,32):
         if span3[d]:continue
         span4=span3.copy()
         for z in range(32):
          if span3[z]:span4[z^d]=1
         for e in range(1,32):
          if span4[e]:continue
          for q in range(nc):
           mm=np.uint32(0)
           for ii in range(lens[q]):
            z=points[q,ii];mm|=np.uint32(1)<<np.uint32(mapv(z,a,b,c,d,e))
           if mm==masks[q]:counts[q]+=1
    return counts

def generalized_weights(cols):
    mins=[];dist=[]
    for r in range(1,6):
        H=collections.Counter()
        for U in SUB[r]:H[sum(any(((u&c).bit_count()&1) for u in U) for c in cols)]+=1
        mins.append(min(H));dist.append(dict(sorted(H.items())))
    n=len(cols);dual=sorted(n+1-x for x in range(1,n+1) if x not in set(mins));assert len(dual)==n-5
    return mins,dual,dist

def hull_dim(cols):
    rows=[sum((((c>>bit)&1)<<j) for j,c in enumerate(cols)) for bit in range(5)];gram=[]
    for i in range(5):gram.append(sum((((rows[i]&rows[j]).bit_count()&1)<<j) for j in range(5)))
    return 5-gf2_rank_rows(gram,5)

def code_certificate():
    names=list(CODES);masks=np.array([sum(1<<x for x in CODES[n]) for n in names],dtype=np.uint32)
    points=np.zeros((len(names),31),dtype=np.int64);lens=np.zeros(len(names),dtype=np.int64)
    for i,n in enumerate(names):lens[i]=len(CODES[n]);points[i,:lens[i]]=CODES[n]
    orders=stabilizer_orders(masks,points,lens);res={}
    expected_orders={'13_5_5':48,'16_5_8':322560,'24_5_11':72,'28_5_14':64512}
    for qi,(name,cols) in enumerate(CODES.items()):
        A=weight_enum(cols);D=dual_enum(len(cols),A);gw,dgw,dist=generalized_weights(cols);comp=sorted(set(range(1,32))-set(cols))
        res[name]={'parameters':[len(cols),5,min(k for k,v in A.items() if k and v)],'columns':cols,'punctured_simplex_complement':comp,'weight_enumerator':{str(k):v for k,v in A.items()},'dual_weight_enumerator':{str(k):v for k,v in D.items()},'dual_minimum_distance':min(k for k in D if k),'generalized_hamming_weights':gw,'dual_generalized_hamming_weights':dgw,'subcode_support_distributions':[{str(k):v for k,v in x.items()} for x in dist],'hull_dimension':hull_dim(cols),'automorphism_order':int(orders[qi])}
        assert int(orders[qi])==expected_orders[name]
    assert res['16_5_8']['generalized_hamming_weights']==[8,12,14,15,16]
    assert res['16_5_8']['automorphism_order']==322560
    assert res['24_5_11']['hull_dimension']==0
    assert res['28_5_14']['punctured_simplex_complement']==[3,5,6]
    return {'codes':res,'identifications':{'16_5_8':'RM(1,4), automorphism group AGL(4,2)','28_5_14':'binary simplex [31,5,16] punctured on one projective line; parabolic stabilizer 2^6 GL(2,2) GL(3,2)'},'status':'PASS_COMPLETE_DUALITY_ATLAS'}


def clebsch_columns():
    cols=[]
    for i in range(16):
        v=0
        for j in (i,i^1,i^2,i^4,i^8,i^15):v|=1<<j
        cols.append(v)
    return cols

def fault_constraints(cols):
    classes=collections.defaultdict(list)
    for a,b in itertools.combinations(range(16),2):classes[cols[a]^cols[b]].append((a,b))
    constraints=sorted(set(tuple(sorted(set(p)^set(q))) for c in classes.values() for p,q in itertools.combinations(c,2)))
    assert len(classes)==30 and {len(c) for c in classes.values()}=={4} and len(constraints)==60 and all(len(c)==4 for c in constraints)
    return classes,constraints

def solve_fault_labels(r,threshold):
    cols=clebsch_columns();_,constraints=fault_constraints(cols);q=1<<r;forbidden={x for x in range(q) if x.bit_count()<threshold}
    byv=[[] for _ in range(16)]
    for ci,c in enumerate(constraints):
        for v in c:byv[v].append(ci)
    assign=[None]*16;assign[0]=0;domains=[set(range(q)) for _ in range(16)];domains[0]={0};nodes=0;solution=None
    def propagate(changed,trail):
        queue=list(set(ci for v in changed for ci in byv[v]))
        while queue:
            c=constraints[queue.pop()];un=[v for v in c if assign[v] is None]
            if not un:
                x=0
                for v in c:x^=assign[v]
                if x in forbidden:return False
            elif len(un)==1:
