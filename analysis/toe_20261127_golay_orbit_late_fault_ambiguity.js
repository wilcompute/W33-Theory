function badOrbit(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0)),V=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1&&!dot(v,v)),span=(a,b)=>Array.from({length:9},(_,i)=>a.map((x,j)=>m((i%3)*x+Math.floor(i/3)*b[j]))).map(v=>v.join("")).sort().join("|");
let iso=new Set();for(let a of V)for(let b of V)if(a!==b&&!dot(a,b))iso.add(span(a,b));A(iso.size===8,'tetracodes');
let a=[1,0,1,1],b=[0,1,1,2],orbit=new Set();function perms(v){if(!v.length)return [[]];return v.flatMap((x,i)=>perms(v.filter((_,j)=>j!==i)).map(p=>[x,...p]))}
for(let p of perms([0,1,2,3]))for(let s=0;s<16;s++){let f=v=>p.map((j,i)=>m(v[j]*((s>>i&1)?2:1)));orbit.add(span(f(a),f(b)))}A(orbit.size===iso.size&&[...orbit].every(x=>iso.has(x)),'orbit');
let rank=9072,localDim=9**7,subsets=792;
return {tetracode_maximal_isotropics:iso.size,signed_permutation_orbit:orbit.size,disjoint_triple_partitions:15400,total_bad_codes:15400*8,all_bad_penalty:"128/81",fourier_companion_product_basis_penalty:subsets*rank/localDim,scope:"Four disjoint triple directions generate U. U-perp/U is F3^4 with negative standard quadratic form. Each bad self-dual code corresponds to one of8 maximal isotropic planes. Permuting inside each triple induces sign changes, permuting blocks permutes coordinates; single orbit, hence all bad codes have same universal diagonal penalty. Fourier-conjugate penalty also annihilates Golay (self-dual), removes every computational-basis product from kernel of sum. No ground space completeness or dissipative gap."}
}
function lateAmbiguity(first){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),sp=(u,v)=>m(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1]),E=[],emap=new Map(),adj=P.map(()=>[]);
for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)if(!sp(P[i],P[j])){emap.set(i+','+j,E.length);E.push([i,j]);adj[i].push(j);adj[j].push(i)}
let e=(a,b)=>emap.get([Math.min(a,b),Math.max(a,b)].join(',')),memZ=[];for(let a=0;a<40;a++)for(let b of adj[a].filter(x=>x>a))for(let c of adj[b].filter(x=>x>b&&adj[a].includes(x))){let z=E.map(()=>0);z[e(a,b)]=1;z[e(b,c)]=1;z[e(a,c)]=2;memZ.push(z)}
let memX=P.map((_,i)=>E.map(([a,b])=>a===i?2:b===i?1:0)),ms=[e(0,1),e(0,13),e(1,4),e(4,13)],sg=[2,1,2,2],Q=P[0].flatMap((_,i)=>P[0].slice(i).map((_,j)=>P.map(v=>m(v[i]*v[i+j])))),ps=P.map((v,i)=>v[2]===0&&v[3]===0?i:-1).filter(i=>i>=0);
function echelon(M){let R=[],p=[];for(let v of M){let r=v.slice();for(let i=0;i<R.length;i++){let f=r[p[i]];if(f)r=r.map((x,j)=>m(x-f*R[i][j]))}let j=r.findIndex(Boolean);if(j>=0){let f=r[j];R.push(r.map(x=>m(x*f)));p.push(j)}}return {R,p}}
let {R,p}=echelon([P.map(()=>1),...Q]);let procZ=[];for(let j=0;j<40;j++)if(!p.includes(j)){let z=P.map(()=>0);z[j]=1;for(let i=p.length-1;i>=0;i--)z[p[i]]=m(-R[i].reduce((s,x,k)=>s+x*z[k],0));procZ.push(z)}
let leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1;
let C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i)))),words=new Map([['000000000000',Array(12).fill(0)]]);
for(let row of C)for(let v of [...words.values()])for(let t=1;t<=2;t++){let a=v.map((x,i)=>m(x+t*row[i]));words.set(a.join(''),a)}
A(words.size===729,'Golay');let short=[...words.values()].filter(x=>!x[0]).map(v=>v.slice(1)),gX=echelon(short).R,gZ=gX;
let gLogical=[...words.values()].find(x=>x[0]===1&&x.filter(Boolean).length===6).slice(1),gs=gLogical.map((x,i)=>x?i:-1).filter(i=>i>=0);A(gs.length===5&&gX.length===5,'Golay logical');
let dot=(a,b)=>m(a.reduce((s,x,i)=>s+x*b[i],0));
let X=first==="memory"?memX:first==="processor"?Q:gX,Z=first==="memory"?memZ:first==="processor"?procZ:gZ,N=X[0].length,joint=null,logicalZ=Array(N).fill(0);
if(first==="memory"){
ms.forEach((v,i)=>logicalZ[v]=sg[i]);for(let i=0;i<40&&!joint;i++)for(let j of adj[i]){let line=P.map((v,k)=>k).filter(k=>[0,1,2].some(a=>[0,1,2].some(b=>P[i].every((x,l)=>m(a*x+b*P[j][l])===P[k][l]))));let v=memX[i].map((c,k)=>E[k].every(x=>line.includes(x))?c:0);if(dot(v,logicalZ)&&Z.every(z=>!dot(v,z))){joint=v.map(x=>m(x*dot(v,logicalZ)));break}}
}else if(first==="processor"){
ps.forEach(i=>logicalZ[i]=1);let best=41;for(let c=0;c<3**Q.length;c++){let a=Array.from({length:Q.length},(_,i)=>Math.floor(c/3**i)%3),v=P.map((_,i)=>m(1+Q.reduce((s,r,k)=>s+a[k]*r[i],0))),w=v.filter(Boolean).length;if(w<best){best=w;joint=v}}A(best===13,'processor distance');
}else{logicalZ=gLogical;joint=gLogical.map(x=>m(2*x))}
A(joint&&dot(joint,logicalZ)===1&&Z.every(z=>!dot(z,joint))&&X.every(x=>Z.every(z=>!dot(x,z))),'CSS logical X');
let as=joint.map((v,i)=>v?i:-1).filter(i=>i>=0);

let b=echelon(X.concat([joint])),zBasis=echelon(Z),red=(v,b)=>{let r=v.slice();for(let i=0;i<b.R.length;i++){let f=r[b.p[i]];if(f)r=r.map((x,j)=>m(x-f*b.R[i][j]))}return r};
let logical=null,type=first==="memory"?"X":"Z",stabilizers=type==="X"?b:zBasis,checks=type==="X"?Z:X;
if(first==="processor")logical=logicalZ;else{
for(let i=0;i<40&&!logical;i++)for(let j of adj[i]){let line=P.map((v,k)=>k).filter(k=>[0,1,2].some(a=>[0,1,2].some(b=>P[i].every((x,l)=>m(a*x+b*P[j][l])===P[k][l]))));let v=memX[i].map((c,k)=>E[k].every(x=>line.includes(x))?c:0);if(v.filter(Boolean).length===3&&checks.every(z=>!dot(z,v))&&red(v,stabilizers).some(Boolean)){logical=v;break}}
}
A(logical&&red(logical,stabilizers).some(Boolean)&&checks.every(v=>!dot(v,logical)),'logical witness');let ix=logical.map((x,i)=>x?i:-1).filter(i=>i>=0),a=Array(N).fill(0),c=a.slice();
if(ix.length===3){a[ix[0]]=logical[ix[0]];a[ix[1]]=m(2*logical[ix[1]]);c[ix[1]]=logical[ix[1]];c[ix[2]]=m(-logical[ix[2]])}else{for(let i of ix.slice(0,2))a[i]=logical[i];for(let i of ix.slice(2))c[i]=m(-logical[i])}
A(a.filter(Boolean).length===2&&c.filter(Boolean).length===2&&a.every((x,i)=>m(x-c[i])===logical[i])&&checks.every(v=>dot(v,a)===dot(v,c)),'ambiguity');
return {first,type,logical_support:ix.map(i=>[i,logical[i]]),error_A:ix.filter(i=>a[i]).map(i=>[i,a[i]]),error_B:ix.filter(i=>c[i]).map(i=>[i,c[i]]),common_syndrome:checks.map(v=>dot(v,a)),scope:"Two final-idle distinct-location double-fault histories, both recorded syndrome and flags zero, parity unchanged, identical even ideal terminal syndrome if measured after faults. Difference is nontrivial logical modulo measured X. No deterministic recovery can correct both. Does not exclude distance-3 fault tolerance (one-fault criterion) or known erasures."}
}

console.log(JSON.stringify({badOrbit:badOrbit(),ambiguity:['memory','processor'].map(lateAmbiguity)},null,2));
