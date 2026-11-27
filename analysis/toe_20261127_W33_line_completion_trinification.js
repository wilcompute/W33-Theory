function bridge(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),idx=new Map(P.map((v,i)=>[v.join(''),i])),can=v=>v.map(x=>m(x*v.find(Boolean))),lines=new Map();
for(let i=0;i<40;i++)for(let j=i+1;j<40;j++){let u=P[i],v=P[j],l=[i,j,idx.get(can(u.map((x,k)=>m(x+v[k]))).join('')),idx.get(can(u.map((x,k)=>m(x-v[k]))).join(''))].sort((a,b)=>a-b);lines.set(l.join(','),{l,iso:!m(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])})}
const row=l=>P.map((_,i)=>+l.includes(i)),all=[...lines.values()].map(x=>row(x.l)),iso=[...lines.values()].filter(x=>x.iso).map(x=>row(x.l)),other=[...lines.values()].filter(x=>!x.iso).map(x=>row(x.l));
const rank=(M,p=3)=>{M=M.map(x=>x.slice());let r=0,mod=x=>((x%p)+p)%p;for(let j=0;j<M[0].length;j++){let k=M.findIndex((x,i)=>i>=r&&Math.abs(x[j])>1e-8);if(k<0)continue;[M[r],M[k]]=[M[k],M[r]];let c=M[r][j];M[r]=M[r].map(x=>p?mod(x*(c===2?2:1)):x/c);for(let i=r+1;i<M.length;i++){let f=M[i][j];M[i]=M[i].map((x,k)=>p?mod(x-f*M[r][k]):x-f*M[r][k])}r++}return r};
let diff=M=>M.slice(1).map(x=>x.map((v,i)=>m(v-M[0][i]))),ra=rank(all),ri=rank(iso),ro=rank(other),rd=rank(diff(all)),rid=rank(diff(iso));A(ra===30&&rd===29,'line generation');
let span=diff(iso),selected=[];for(let i=0;i<other.length;i++){let d=other[i].map((x,j)=>m(x-iso[0][j]));if(rank(span.concat([d]))>rank(span)){span.push(d);selected.push(i)}}
A(rank(span)===29,'completion');
let E=(i,j)=>Array.from({length:3},(_,u)=>Array.from({length:3},(_,v)=>+(u===i&&v===j))),zero=E(9,9),gen=[];for(let i=0;i<3;i++)for(let j=0;j<3;j++)if(i!==j)gen.push(E(i,j));gen.push(E(0,0).map((r,i)=>r.map((x,j)=>x-E(1,1)[i][j])),E(1,1).map((r,i)=>r.map((x,j)=>x-E(2,2)[i][j])));
const mul=(a,b)=>a.map(r=>b[0].map((_,j)=>r.reduce((s,x,k)=>s+x*b[k][j],0))),sub=(a,b)=>a.map((r,i)=>r.map((x,j)=>x-b[i][j])).flat(),tr=a=>a[0].map((_,i)=>a.map(r=>r[i])),vs=[E(2,1),E(2,2)],M=[],M0=[];
for(let side of [0,1])for(let g of gen){let a=side?zero:g,b=side?g:zero,L=vs.flatMap(v=>sub(mul(a,v),mul(v,b))),R=vs.flatMap(v=>sub(mul(b,tr(v)),mul(tr(v),a)));M0.push(L);M.push(L.concat(R))}
let br=rank(M,0);A(br===12,'SM centralizer');
let L=[-1,-1,2],R=[-4,2,2],charges={};function add(k){charges[k]=(charges[k]||0)+1}
for(let i=0;i<3;i++){add(`3,${i===2?1:2},${-L[i]}`);add(`3bar,1,${R[i]}`);for(let j=0;j<3;j++)add(`1,${i===2?1:2},${L[i]-R[j]}`)}
let multiplets={};for(let [k,n] of Object.entries(charges))multiplets[k]=n/(k.split(',')[1]==='2'?2:1);
return {line_span:{projective:ra,isotropic:ri,nonisotropic:ro,all_difference_rank:rd,isotropic_difference_rank:rid,additional_nonisotropic_checks:selected.length,selected_nonisotropic_indices:selected,intermediate_logical_count:40-10-rid,full_logical_count:1},trinification:{VEV_positions:[[2,1],[2,2]],complex_stabilizer_without_duals:16-rank(M0,0),broken_generator_rank:br,unbroken_LR:16-br,total_unbroken:8+16-br,hypercharge_in_units_of_one_sixth:{L,R},multiplets_per27:multiplets,scope:'chosen pair of rank-one neutral VEVs, D-flat with conjugates and F-flat for pure cubic; mixed singlet terms may lift'}}
}
console.log(JSON.stringify(bridge(),null,2));
