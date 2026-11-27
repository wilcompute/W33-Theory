function e6(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),key=x=>x.join(','),roots=[];
for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)for(let s of [-2,2])for(let t of [-2,2]){let r=Array(8).fill(0);r[i]=s;r[j]=t;roots.push(r)}
for(let i=0;i<256;i++){let r=Array.from({length:8},(_,j)=>i>>j&1?-1:1);if(r.filter(x=>x<0).length%2===0)roots.push(r)}
A(roots.length===240,'E8');
let R=roots.filter(r=>r[0]===r[1]&&r[1]===r[2]);A(R.length===72,'E6');
const pos=R.filter(r=>r.find(x=>x)!==undefined&&r.find(x=>x)>0),ps=new Set(pos.map(key)),simple=pos.filter(r=>!pos.some(s=>ps.has(key(r.map((x,i)=>x-s[i])))));
A(simple.length===6,'simple roots');
const C=simple.map(r=>simple.map(s=>dot(r,s)/4)),vec=Array.from({length:729},(_,i)=>Array.from({length:6},(_,j)=>Math.floor(i/3**j)%3)),id=v=>v.reduce((s,x,i)=>s+x*3**i,0);
let W=roots.filter(r=>r[0]-r[1]===2&&r[1]-r[2]===0);A(W.length===27,'27 weights');
let orbs=[],seen=new Set();
for(let v of vec){if(seen.has(id(v)))continue;let Q=[v],S=new Set([id(v)]);for(let i=0;i<Q.length;i++)for(let j=0;j<6;j++){let q=Q[i].slice();q[j]=m(q[j]-dot(C[j],q));let k=id(q);if(!S.has(k)){S.add(k);Q.push(q)}}
for(let k of S)seen.add(k);
let co=Array.from({length:8},(_,i)=>simple.reduce((s,r,j)=>s+v[j]*r[i],0)),Z=R.filter(r=>m(dot(r,co)/4)===0),wh=[0,0,0];W.forEach(r=>wh[m(dot(r,co)/4)]++);
let rootSet=new Set(Z.map(key)),p=Z.filter(r=>r.find(x=>x)>0),pS=new Set(p.map(key)),b=p.filter(r=>!p.some(s=>pS.has(key(r.map((x,i)=>x-s[i]))))),cs=[],vis=new Set();for(let j=0;j<b.length;j++){if(vis.has(j))continue;let q=[j];vis.add(j);for(let k=0;k<q.length;k++)for(let l=0;l<b.length;l++)if(!vis.has(l)&&dot(b[q[k]],b[l])!==0){vis.add(l);q.push(l)}cs.push({rank:q.length,edges:q.flatMap((i,k)=>q.slice(k+1).filter(j=>dot(b[i],b[j])!==0).map(j=>[i,j])),degrees:q.map(i=>q.filter(j=>i!==j&&dot(b[i],b[j])!==0).length).sort()})}
orbs.push({cocharacter:v,orbit_size:S.size,unbroken_roots:Z.length,rank:b.length,abelian_rank:6-b.length,components:cs.map(c=>({rank:c.rank,degrees:c.degrees})),weights27:wh,charged_multiplet_components:{matter:wh.reduce((s,x,i)=>s+x*[9,7,7][i],0),conjugate:wh.reduce((s,x,i)=>s+x*[6,4,4][i],0),net:81}})}
A(seen.size===729,'Weyl coverage');
return {simple_roots_scaled2:simple,cartan:C,orbits:orbs,orbit_count:orbs.length,order3_nonidentity:728}
}
console.log(JSON.stringify(e6(),null,2));
