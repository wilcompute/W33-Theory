function architecture(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),n=40,idx=new Map(P.map((v,i)=>[v.join(''),i])),can=v=>v.map(x=>m(x*v.find(Boolean))),dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),diff=(a,b)=>a.map((x,i)=>m(x-b[i])),ones=P.map(()=>1),L=new Map();
for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){let u=P[i],v=P[j],l=[i,j,idx.get(can(u.map((x,k)=>m(x+v[k]))).join('')),idx.get(can(u.map((x,k)=>m(x-v[k]))).join(''))].sort((a,b)=>a-b);L.set(l.join(','),{l,iso:!m(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])})}
let lines=[...L.values()],row=l=>P.map((_,i)=>+l.includes(i)),r=lines.map(x=>row(x.l)),Q=P[0].flatMap((_,i)=>P[0].slice(i).map((_,j)=>P.map(v=>m(v[i]*v[i+j]))));
function rref(M){M=M.map(x=>x.slice());let t=0,p=[];for(let j=0;j<M[0].length;j++){let k=M.findIndex((x,i)=>i>=t&&x[j]);if(k<0)continue;[M[t],M[k]]=[M[k],M[t]];let c=M[t][j];M[t]=M[t].map(x=>m(x*c));for(let i=0;i<M.length;i++)if(i!==t){let f=M[i][j];M[i]=M[i].map((x,k)=>m(x-f*M[t][k]))}p.push(j);t++}return {M,p,rank:t}}
let basis=[],selected=[],loads=Array(n).fill(0);
function add(native,target){let C=[];for(let i=0;i<130;i++)for(let j=i+1;j<130;j++){if(native&&(!lines[i].iso||!lines[j].iso))continue;let v=diff(r[i],r[j]);if(v.filter(Boolean).length!==6)continue;C.push({i,j,v})}while(basis.length<target){C.sort((a,b)=>a.v.reduce((s,x,i)=>s+(x?loads[i]:0),0)-b.v.reduce((s,x,i)=>s+(x?loads[i]:0),0));let k=C.findIndex(c=>rref(basis.concat([c.v])).rank>basis.length);A(k>=0,'rank completion');let c=C.splice(k,1)[0];basis.push(c.v);selected.push([c.i,c.j]);c.v.forEach((x,i)=>{if(x)loads[i]++})}}
add(true,24);add(false,29);A(basis.every(z=>!dot(z,ones)&&Q.every(x=>!dot(z,x))),'Z commutation');
let zL=r[0],constraints=basis.concat([zL]),gauge=[];
for(let j=0;j<5;j++){let rhs=constraints.map((_,i)=>+(i===24+j)),R=rref(constraints.map((x,i)=>x.concat(rhs[i]))),v=Array(n).fill(0);R.p.forEach((p,i)=>{A(p<n,'consistent');v[p]=R.M[i][n]});A(constraints.every((x,i)=>dot(x,v)===rhs[i]),'dual');gauge.push(v)}
let branches=0;for(let a=0;a<243;a++){let s=Array.from({length:5},(_,i)=>Math.floor(a/3**i)%3),v=P.map((_,i)=>m(-s.reduce((t,x,j)=>t+x*gauge[j][i],0)));A(basis.every((x,i)=>dot(x,v)===(i<24?0:m(-s[i-24])))&&!dot(v,zL),'fix');branches++}
let gates=0;for(let x of [ones,...Q])for(let y of [ones,...Q]){A(dot(x,y)===+(x===ones&&y===ones),'transversal CZ');gates++}
let teleport=0;for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let t=0;t<3;t++){A(m(a*b-t*a+t*a)===m(a*b),'Fourier');teleport++}
let pauli=[];for(let i=0;i<n;i++)for(let a=0;a<3;a++)for(let b=0;b<3;b++)if(a||b){let sx=basis.map(z=>m(a*z[i])),sz=Q.map(x=>m(b*x[i]));A(sx.some(Boolean)||sz.some(Boolean),'single detect');pauli.push({i,a,b,key:sx.concat(sz).join('')})}
A(new Set(pauli.map(e=>e.key)).size===320,'single correction');
let R=rref([ones,...Q]),encoding=R.M.slice(0,11).reduce((s,row,i)=>s+row.filter((x,j)=>x&&!R.p.includes(j)).length,0);
return {line_checks:selected.map(([i,j])=>({plus:lines[i],minus:lines[j]})),weights:basis.map(x=>x.filter(Boolean).length),loads,ancilla_data_SUMs_per_round:174,fix_gauge_vectors:gauge,fix_branches:branches,logical_CZ_bilinear_tests:gates,Fourier_teleport_phase_tests:teleport,unique_single_pauli_syndromes:320,systematic_encoder_SUM_count:encoding,physical_modes:{single_photon_full_block:(3n**40n).toString(),one_qutrit_per_photon:120,three_blocks:360},scope:'ideal check projections and encoded teleportation, single Pauli syndrome enumeration; no noisy verified cat preparation or circuit threshold'}
}
console.log(JSON.stringify(architecture(),null,2));
