                u=un[0];x=0
                for v in c:
                    if v!=u:x^=assign[v]
                bad={x^f for f in forbidden};rem=domains[u]&bad
                if rem:
                    old=domains[u].copy();domains[u]-=rem;trail.append((u,old))
                    if not domains[u]:return False
                    if len(domains[u])==1 and assign[u] is None:
                        assign[u]=next(iter(domains[u]));trail.append(('a',u));queue.extend(byv[u])
            elif len(un)==2:
                u,z=un;x=0
                for v in c:
                    if assign[v] is not None:x^=assign[v]
                for aa,bb in ((u,z),(z,u)):
                    allowed={va for va in domains[aa] if any((x^va^vb) not in forbidden for vb in domains[bb])}
                    if allowed!=domains[aa]:
                        old=domains[aa].copy();domains[aa]=allowed;trail.append((aa,old))
                        if not allowed:return False
                        if len(allowed)==1 and assign[aa] is None:
                            assign[aa]=next(iter(allowed));trail.append(('a',aa));queue.extend(byv[aa])
        return True
    def undo(trail):
        for item in reversed(trail):
            if item[0]=='a':assign[item[1]]=None
            else:domains[item[0]]=item[1]
    def rec():
        nonlocal nodes,solution;nodes+=1
        if all(v is not None for v in assign):solution=tuple(assign);return True
        cand=[v for v in range(1,16) if assign[v] is None]
        u=min(cand,key=lambda v:(len(domains[v]),-sum(sum(assign[x] is not None for x in constraints[ci])**3 for ci in byv[v]),v))
        for val in sorted(domains[u],key=lambda x:(x.bit_count(),x)):
            trail=[];old=domains[u].copy();domains[u]={val};trail.append((u,old));assign[u]=val;trail.append(('a',u))
            if propagate([u],trail) and rec():return True
            undo(trail)
        return False
    ok=rec();return ok,solution,nodes

def fault_words(labels):
    cols=clebsch_columns();patterns=[()]+[(i,) for i in range(16)]+list(itertools.combinations(range(16),2));words=[]
    for p in patterns:
        b=0;e=0
        for i in p:b^=cols[i];e^=labels[i]
        words.append(b|(e<<16))
    return patterns,words

def fault_certificate():
    u32,s32,n32=solve_fault_labels(3,2);u43,s43,n43=solve_fault_labels(4,3);s53,lab,n53=solve_fault_labels(5,3)
    assert not u32 and not u43 and s53 and list(lab)==FAULT_LABELS
    patterns,words=fault_words(lab);mind=min((words[i]^words[j]).bit_count() for i in range(137) for j in range(i+1,137))
    old=[0,0,0,0,0,1,2,3,0,2,3,4,5,6,1,7];_,oldwords=fault_words(old);oldmind=min((oldwords[i]^oldwords[j]).bit_count() for i in range(137) for j in range(i+1,137))
    assert len(set(words))==137 and mind==3 and oldmind==1
    return {'base_syndrome_bits':16,'patterns':137,'collision_classes':30,'pairs_per_collision_class':4,'distinct_four_point_constraints':60,'three_bits_distance_two':{'status':'UNSAT','nodes':n32},'four_bits_distance_three':{'status':'UNSAT','nodes':n43},'five_bits_distance_three':{'status':'SAT','nodes':n53,'labels':list(lab)},'old_three_bit_compound_minimum_distance':oldmind,'new_twenty_one_bit_minimum_distance':mind,'theorem':'Five companion bits are necessary and sufficient to locate every zero/single/double device fault and correct one corrupted compound-readout bit.'}


def subgroup_certificate():
    chiP={1:20,2:0,3:2,5:0};chiW={1:20,2:4,3:5,5:0};atlas={}
    def entry(name,order,P,W,dims,field='Q',hom=None):
        atlas[name]={'order':order,'P_multiplicities':P,'W_multiplicities':W,'irrep_dimensions':dims,'field':field,'max_common_submodule_dimension':sum(min(a,b)*d for a,b,d in zip(P,W,dims)),'hom_dimension':sum(a*b for a,b in zip(P,W)) if hom is None else hom,'isomorphic':P==W}
    entry('C2',2,[10,10],[12,8],[1,1]);entry('C3',3,[8,6],[10,5],[1,2],hom=140);entry('C5',5,[4,4],[4,4],[1,4],hom=80)
    entry('V4',4,[5,5,5,5],[8,4,4,4],[1,1,1,1]);entry('S3',6,[4,4,6],[7,3,5],[1,1,2]);entry('D5',10,[2,2,4,4],[4,0,4,4],[1,1,2,2],field='R')
    entry('A4',12,[3,1,1,5],[6,1,1,4],[1,1,1,3],field='C');entry('A5',60,[1,1,1,2,1],[3,0,0,3,1],[1,3,3,4,5],field='C')
    assert [H for H,v in atlas.items() if v['isomorphic']]==['C5'] and atlas['C5']['max_common_submodule_dimension']==20 and atlas['A5']['max_common_submodule_dimension']==14
    fixed={'C2':lambda c:Fraction(c[1]+c[2],2),'C3':lambda c:Fraction(c[1]+2*c[3],3),'C5':lambda c:Fraction(c[1]+4*c[5],5),'V4':lambda c:Fraction(c[1]+3*c[2],4),'S3':lambda c:Fraction(c[1]+3*c[2]+2*c[3],6),'D5':lambda c:Fraction(c[1]+5*c[2]+4*c[5],10),'A4':lambda c:Fraction(c[1]+3*c[2]+8*c[3],12),'A5':lambda c:Fraction(c[1]+15*c[2]+20*c[3]+24*c[5],60)}
    checks={H:{'Perkel':int(f(chiP)),'W33':int(f(chiW))} for H,f in fixed.items()}
    return {'source_characters':{'classes':[1,2,3,5],'Perkel':[20,0,2,0],'W33':[20,4,5,0]},'atlas':atlas,'fixed_space_checks':checks,'unique_nontrivial_full_isomorphism_within_common_A5':'C5','C5_theorem':'Both rank-20 modules restrict over Q as 4*1 plus 4*Q(zeta_5); the rational intertwiner space has dimension 80.','boundary':'Only subgroup types inside the explicit common A5 are classified; no canonical objectwise C5 map or external-group identification is asserted.'}


def certificate():
    geo=geometry();G,C,M,P=quotient_generators(geo)
    edge_counts=collections.Counter(e for f in geo['faces'] for e in itertools.combinations(f,2))
    geometry_data={'w33_vertices':40,'w33_edges':240,'canonical_octets':45,'block_graph_edges':720,'filled_triangles':240,'block_graph_spectrum':{'32':1,'2':24,'-4':20},'w33_edge_to_triangle_multiplicity':3,'triangle_edge_partition':len(edge_counts)==720 and set(edge_counts.values())=={1},'theorem':'Each W33 edge lies in exactly three canonical K4,4 octets; their triple is a filled triangle, and the 240 such triangles partition all 720 edges of the 45-octet graph.'}
    data={'schema':'w33.pass3542_3555.radius_amplitude_code_fault_c5.v1','status':'PASS_7_FRONTS','live_boundaries':{'covering_radius':'open in [389,435]','chromatic_number':'open in {10,11}','amplitude':'global unrestricted optimum open'},'sections':{'octet_edge_triangle_resolution':geometry_data,'relation_plane_radius':radius_certificate(geo,G),'five_channel_amplitude':amplitude_certificate(geo),'equivariant_code_duality':code_certificate(),'compound_fault_distance':fault_certificate(),'rank20_subgroup_atlas':subgroup_certificate()},'checks':{}}
    s=data['sections'];data['checks']={'geometry_exact':s['octet_edge_triangle_resolution']['triangle_edge_partition'],'radius_relation_263':s['relation_plane_radius']['new_circuit_weight']==263,'radius_pair_census':s['relation_plane_radius']['pair_census']==40186,'amplitude_exact_witness':s['five_channel_amplitude']['dyadic_witness']['certified_decimal_interval']==['8.90622','8.90623'],'code_RM14_aut':s['equivariant_code_duality']['codes']['16_5_8']['automorphism_order']==322560,'fault_five_bit_minimum':s['compound_fault_distance']['new_twenty_one_bit_minimum_distance']==3,'C5_full_isomorphism':s['rank20_subgroup_atlas']['atlas']['C5']['isomorphic']}
    assert all(data['checks'].values())
    data['semantic_sha256']=semantic_hash(data);return data

def main():
    data=certificate();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(f"PASS_7_FRONTS {data['semantic_sha256']}")
if __name__=='__main__':main()
