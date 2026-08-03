#!/usr/bin/env python3
"""Pass 2774: W33-line x symmetric-form structured CX compiler and SV generator."""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from bt2772_2776_core import *
ROOT=Path(__file__).resolve().parents[1]
def pack_mat(A):return sum((int(x)%3)<<(2*i) for i,x in enumerate([x for row in A for x in row]))
def pack_vec(v):return sum((int(x)%3)<<(2*i) for i,x in enumerate(v))
def mat_np(g):return np.array(g,dtype=int)%3
def image_line(N):
    basis=[]
    for j in range(4):
        c=tuple(int(x) for x in N[:,j]%3)
        if not any(c):continue
        if rank3(np.column_stack([np.array(x) for x in basis+[c]]))>len(basis):basis.append(c)
        if len(basis)==2:break
    assert len(basis)==2
    return tuple(sorted({norm3(tuple((a*np.array(basis[0])+b*np.array(basis[1]))%3)) for a,b in itertools.product(range(3),repeat=2) if a or b}))
def form_key(S):return (int(S[0,0]),int(S[0,1]),int(S[1,1]))
def main():
    group,parent=group_closure(with_parent=True);C=centralizer(group);z6,z3,s3a,s3b,S3=factor_centralizer(C);points,lines=w33_lines();frames=[canonical_line_frame(L) for L in lines];lidx={L:i for i,L in enumerate(lines)}
    forms=sorted((a,b,c) for a,b,c in itertools.product(range(3),repeat=3) if (a*c-b*b)%3==2);assert len(forms)==12;fidx={x:i for i,x in enumerate(forms)};pair_to_rep={};pair_to_h={}
    for g in group:
        h=mm(mm(g,CX),inv(g));N=(mat_np(h)-np.eye(4,dtype=int))%3;L=image_line(N);li=lidx[L];B,M=frames[li];K=inv3(np.column_stack([B,M]))[:2,:];S=(K@N@M)%3;assert np.array_equal(S,S.T) and int(round(np.linalg.det(S)))%3==2;pair=(li,fidx[form_key(S)])
        if pair not in pair_to_rep:pair_to_rep[pair]=g;pair_to_h[pair]=h
        else:assert pair_to_h[pair]==h
    assert len(pair_to_rep)==480 and set(pair_to_rep)==set(itertools.product(range(40),range(12)));reps=[pair_to_rep[(li,fi)] for li in range(40) for fi in range(12)]
    suffix=[];suffix_coords=[]
    for a in range(6):
        for b in range(3):
            for si,s in enumerate(S3):suffix.append(mm(mm(mpow(z6,a),mpow(z3,b)),s));suffix_coords.append((a,b,si))
    assert len(set(suffix))==108 and set(suffix)==set(C);sidx={c:i for i,c in enumerate(suffix)};checks=0
    for g in group:
        h=mm(mm(g,CX),inv(g));N=(mat_np(h)-np.eye(4,dtype=int))%3;L=image_line(N);li=lidx[L];B,M=frames[li];K=inv3(np.column_stack([B,M]))[:2,:];S=K@N@M%3;fi=fidx[form_key(S)];r=pair_to_rep[(li,fi)];c=mm(inv(r),g);assert c in sidx and mm(g,CX)==mm(mm(r,CX),c);checks+=1
    dense=51840*16;line_frame_bits=40*16*2;form_bits=12*3*2;rep_inverse_bits=480*16*2;suffix_matrix_bits=108*16*2;structured=line_frame_bits+form_bits+rep_inverse_bits+suffix_matrix_bits
    out={'schema':'w33.pass2774.structured_cx_compiler.v1','status':'EXACT_51840_COMPLETE','factorization':{'cosets':'40 W33 Lagrangian lines x 12 invertible symmetric 2x2 forms of determinant 2','centralizer':'C6 x C3 x S3','cosets':480,'suffixes':108},'checks':{'group_elements':checks,'all_pairs_present':True,'all_rewrites_verified':True},'memory_bits':{'dense_51840x16_dispatch':dense,'line_frames':line_frame_bits,'form_dictionary':form_bits,'representative_inverses':rep_inverse_bits,'centralizer_matrices':suffix_matrix_bits,'structured_total':structured,'compression_ratio':dense/structured},'forms':forms,'line_frames':[{'line_id':i,'points':[list(p) for p in lines[i]],'B':B.tolist(),'M':M.tolist(),'K':inv3(np.column_stack([B,M]))[:2,:].tolist()} for i,(B,M) in enumerate(frames)],'representatives':[{'coset_id':i,'line_id':i//12,'form_id':i%12,'representative':[list(row) for row in reps[i]],'inverse':[list(row) for row in inv(reps[i])]} for i in range(480)],'centralizer_suffixes':[{'suffix_id':i,'coordinates':{'c6_power':a,'c3_power':b,'s3_index':si},'matrix':[list(row) for row in suffix[i]]} for i,(a,b,si) in enumerate(suffix_coords)],'boundary':'The generated decoder accepts the accumulated gate matrix g and its CX conjugate h=g CX g^-1. The group accumulator remains responsible for producing those exact matrices; invalid/non-CX-class conjugates fail closed.'}
    path=ROOT/'data/PART_BT2774_STRUCTURED_CX_COMPILER.json';path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');generate_sv(out,ROOT/'rtl/w33_pass2774_structured_cx_decoder.sv');summary={k:out[k] for k in ('schema','status','checks','factorization','memory_bits','boundary')};(ROOT/'data/PART_BT2774_STRUCTURED_CX_COMPILER_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print('wrote',path)
def generate_sv(out,path):
    frames=out['line_frames'];reps=out['representatives'];suffix=out['centralizer_suffixes'];forms=out['forms'];L=[];A=L.append
    A('// Auto-generated Pass 2774 structured CX decoder.');A('module w33_pass2774_structured_cx_decoder(input logic [31:0] g_matrix,input logic [31:0] conjugate_matrix,output logic valid,output logic [8:0] coset_id,output logic [6:0] suffix_id);');A('integer i,j,k,li,matches; logic [31:0] nmat,rep_inv,cmat; logic [7:0] col,ncol; logic [5:0] line_id; logic [3:0] form_id;');A('logic [1:0] Krom[0:39][0:7]; logic [1:0] Mrom[0:39][0:7]; logic [7:0] Lpts[0:39][0:3]; logic [31:0] Rinv[0:479]; logic [31:0] Ctab[0:107];');A('function automatic [1:0] t(input logic [31:0] x,input integer q); t=x[2*q +: 2]; endfunction');A('function automatic [1:0] add3(input [1:0] a,b); integer s; begin s=a+b; add3=(s>=3)?s-3:s; end endfunction');A('function automatic [1:0] mul3(input [1:0] a,b); mul3=(a*b)%3; endfunction');A('function automatic [7:0] normv(input [7:0] v); integer q; logic [1:0] f; begin f=0; for(q=0;q<4;q=q+1) if(f==0&&v[2*q +:2]!=0) f=v[2*q +:2]; normv=v; if(f==2) for(q=0;q<4;q=q+1) normv[2*q +:2]=mul3(v[2*q +:2],2); end endfunction');A('initial begin')
    for fr in frames:
        li=fr['line_id']
        for q,p in enumerate(fr['points']):A(f"Lpts[{li}][{q}]=8'h{pack_vec(p):02x};")
        for q,v in enumerate(sum(fr['K'],[])):A(f"Krom[{li}][{q}]=2'd{v};")
        for q,v in enumerate(sum(fr['M'],[])):A(f"Mrom[{li}][{q}]=2'd{v};")
    for r in reps:A(f"Rinv[{r['coset_id']}]=32'h{pack_mat(r['inverse']):08x};")
    for c in suffix:A(f"Ctab[{c['suffix_id']}]=32'h{pack_mat(c['matrix']):08x};")
    A('end');A('logic [1:0] S00,S01,S10,S11,acc; logic in_line,nonzero;');A('always_comb begin valid=0;coset_id=0;suffix_id=0;nmat=conjugate_matrix;nmat[1:0]=add3(t(conjugate_matrix,0),2);nmat[11:10]=add3(t(conjugate_matrix,5),2);nmat[21:20]=add3(t(conjugate_matrix,10),2);nmat[31:30]=add3(t(conjugate_matrix,15),2);matches=0;line_id=0;');A('for(li=0;li<40;li=li+1) begin in_line=1;for(j=0;j<4;j=j+1) begin col=0;nonzero=0;for(i=0;i<4;i=i+1) begin col[2*i +:2]=t(nmat,4*i+j);if(t(nmat,4*i+j)!=0) nonzero=1;end ncol=normv(col);if(nonzero&&!(ncol==Lpts[li][0]||ncol==Lpts[li][1]||ncol==Lpts[li][2]||ncol==Lpts[li][3])) in_line=0;end if(in_line) begin matches=matches+1;line_id=li[5:0];end end');A('S00=0;S01=0;S10=0;S11=0;for(i=0;i<4;i=i+1)for(j=0;j<4;j=j+1)begin S00=add3(S00,mul3(Krom[line_id][i],mul3(t(nmat,4*i+j),Mrom[line_id][2*j])));S01=add3(S01,mul3(Krom[line_id][i],mul3(t(nmat,4*i+j),Mrom[line_id][2*j+1])));S10=add3(S10,mul3(Krom[line_id][4+i],mul3(t(nmat,4*i+j),Mrom[line_id][2*j])));S11=add3(S11,mul3(Krom[line_id][4+i],mul3(t(nmat,4*i+j),Mrom[line_id][2*j+1])));end form_id=15;case({S00,S01,S11})')
    for fi,(a,b,c) in enumerate(forms):A(f"6'b{a:02b}{b:02b}{c:02b}:form_id=4'd{fi};")
    A('default:form_id=15;endcase coset_id=line_id*12+form_id;rep_inv=Rinv[coset_id];cmat=0;for(i=0;i<4;i=i+1)for(j=0;j<4;j=j+1)begin acc=0;for(k=0;k<4;k=k+1)acc=add3(acc,mul3(t(rep_inv,4*i+k),t(g_matrix,4*k+j)));cmat[2*(4*i+j)+:2]=acc;end for(i=0;i<108;i=i+1)if(cmat==Ctab[i])begin suffix_id=i[6:0];valid=(matches==1&&form_id<12);end end endmodule');path.write_text('\n'.join(L)+'\n')
if __name__=='__main__':main()
