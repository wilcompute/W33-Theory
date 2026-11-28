function rank4Actual(table,prior,n=10){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},leg=x=>[1,3,4,5,9].includes((x%11+11)%11)?1:-1,C=Array.from({length:12},(_,i)=>Array.from({length:12},(_,j)=>m(i===j?1:i===0?1:j===0?-1:leg(j-i))));
function basis(rows,p=3){let R=[],piv=[];for(let a of rows){let v=a.slice();for(let i=0;i<R.length;i++){let f=v[piv[i]];if(f)v=v.map((x,j)=>(x-f*R[i][j]+p*p)%p)}let k=v.findIndex(Boolean);if(k>=0){let inv=1;while(inv*v[k]%p!==1)inv++;R.push(v.map(x=>x*inv%p));piv.push(k)}}return R}
let B=basis(C),words=[Array(12).fill(0)];for(let r of B)words=words.flatMap(v=>[0,1,2].map(t=>v.map((x,i)=>m(x+t*r[i]))));let ones=words.find(v=>v.every(Boolean));B=B.map(v=>v.map((x,i)=>m(x*ones[i])));A(B.length===6&&words.filter(v=>v.some(Boolean)).every(v=>v.filter(Boolean).length>=6),"Golay");
const mod=x=>(x%11+11)%11,inv=x=>Array.from({length:10},(_,i)=>i+1).find(y=>mod(x*y)===1),G=new Map();
for(let a=0;a<11;a++)for(let b=0;b<11;b++)for(let c=0;c<11;c++)for(let d=0;d<11;d++)if(mod(a*d-b*c)){let p=Array.from({length:12},(_,x)=>{let u=x===11?a:mod(a*x+b),v=x===11?c:mod(c*x+d);return v?mod(u*inv(v)):11});G.set(p.join(","),p)}
let P=[...G.values()];A(P.length===1320&&new Set(P.map(p=>p.slice(0,3).join(","))).size===1320,"3transitive");
const mask=4095,pack=v=>v.reduce((s,x,i)=>s|((x===1?1:x===2?4096:0)<<i),0),neg=x=>((x&mask)<<12)|(x>>>12);
function add(x,y){let a=x&mask,b=x>>>12,c=y&mask,d=y>>>12;return (((a&~(c|d))|(c&~(a|b))|(b&d))&mask)|((((b&~(c|d))|(d&~(a|b))|(a&c))&mask)<<12)}
function canonical(rows){let r=rows.slice(),n=0;for(let j=0;j<12;j++){let b=1<<j,k=r.findIndex((x,i)=>i>=n&&((x|x>>>12)&b));if(k<0)continue;[r[n],r[k]]=[r[k],r[n]];if(r[n]&(b<<12))r[n]=neg(r[n]);for(let i=0;i<r.length;i++)if(i!==n){if(r[i]&b)r[i]=add(r[i],neg(r[n]));else if(r[i]&(b<<12))r[i]=add(r[i],r[n])}n++}return r.slice(0,n)}

let samples=prior.sample_bases.slice(0,n),packed=samples.map(b=>b.map(pack)),orbits=samples.map(b=>{let set=new Map();for(let p of P){let r=canonical(b.map(v=>p.map(i=>v[i])).map(pack));set.set(r.join(","),r)}return [...set.values()]});
let quads=[],det=(a,b)=>((a===11?1:a)*(b===11?0:1)-(a===11?0:1)*(b===11?1:b)+121)%11,iv=x=>Array.from({length:10},(_,i)=>i+1).find(y=>x*y%11===1);
for(let i=0;i<12;i++)for(let j=i+1;j<12;j++)for(let k=j+1;k<12;k++)for(let l=k+1;l<12;l++){let cr=det(l,j)*det(k,i)*iv(det(l,i)*det(k,j)%11)%11;A(cr>=2&&cr<=10,"cross ratio");quads.push([i,j,k,l,(cr-2)*80])}
const ker=Array.from({length:27},(_,i)=>{let a=[i%3,Math.floor(i/3)%3,Math.floor(i/9)],v=0;for(let j=0;j<27;j++)if(!m(a[0]*(j%3)+a[1]*(Math.floor(j/3)%3)+a[2]*Math.floor(j/9)))v|=1<<j;return v}),types=new Map();table.types.forEach((t,i)=>{if(!types.has(t.mask))types.set(t.mask,{index:i,B:t.B})});
let full=types.get((1<<27)-1);A(full.B.length===3,"full");
let val=(v,j)=>(v>>j&1)+2*(v>>(12+j)&1);
function hist(b,c,H){let r=b.concat(c),d=b.map(()=>0).concat(c),h=0,p=[];for(let j=0;j<12;j++){let bit=1<<j,k=r.findIndex((x,i)=>i>=h&&((x|x>>>12)&bit));if(k<0)continue;[r[h],r[k]]=[r[k],r[h]];[d[h],d[k]]=[d[k],d[h]];if(r[h]&(bit<<12)){r[h]=neg(r[h]);d[h]=neg(d[h])}for(let i=h+1;i<r.length;i++){if(r[i]&bit){r[i]=add(r[i],neg(r[h]));d[i]=add(d[i],neg(d[h]))}else if(r[i]&(bit<<12)){r[i]=add(r[i],r[h]);d[i]=add(d[i],d[h])}}p.push(j);h++}
let rem=[],part=[];for(let k=0;k<12;k++){let u=1<<k,t=0;for(let i=0;i<h;i++){let bit=1<<p[i];if(u&bit){u=add(u,neg(r[i]));t=add(t,d[i])}else if(u&(bit<<12)){u=add(u,r[i]);t=add(t,neg(d[i]))}}rem.push(u);part.push(t)}
let free=Array.from({length:12},(_,i)=>i).filter(i=>!p.includes(i)),rr=rem.map(v=>free.map(j=>val(v,j))),dd=part.map(v=>Array.from({length:12},(_,j)=>val(v,j))),w=3**(2*(11-h));
let ph=(i,j,l)=>m(2-dd[i][j]+dd[l][j]+dd[i][l]-dd[l][l]);
for(let [i,j,k,l,cr] of quads){let type=full;if(h<11){let mask=(1<<27)-1;for(let a=0;a<free.length;a++){let base=rr[l][a],u=m(rr[i][a]-base)+3*m(rr[j][a]-base)+9*m(rr[k][a]-base);mask&=ker[u]}type=types.get(mask);A(type,"kernel")}
let dim=type.B.length,idx=type.index;if(dim===3)idx+=ph(i,j,l)+3*ph(i,k,l)+9*ph(j,k,l);else if(dim===2){let [a,b]=type.B,sites=[i,j,k],sa=a.reduce((x,y)=>x+y,0),sb=b.reduce((x,y)=>x+y,0),q=2*(a.reduce((s,x,t)=>s+x*b[t],0)+sa*sb);for(let u=0;u<3;u++)for(let v=0;v<3;v++)q-=a[u]*b[v]*(dd[sites[u]][sites[v]]-dd[l][sites[v]]-dd[sites[u]][l]+dd[l][l]);idx+=m(q)}H[cr+idx]+=w}
}
let rows=[],pairs=[];for(let i=0;i<n;i++)for(let j=i;j<n;j++){let H=new Float64Array(720),o=orbits[j];for(let c of o)hist(packed[i],c,H);let v=Array(43).fill(0);for(let k=0;k<720;k++)if(H[k])for(let l=0;l<43;l++)v[l]+=H[k]*table.table[k][l];v=v.map(x=>x*1320/o.length);A(v[0]===prior.gram[i][j]*24*495,"identity crosscheck");for(let k=0;k<4;k++){let scale=k===0?66:k===3?440:220;A(v[k+1]*scale===prior.compression_numerators[k][i][j]*48*495,"lower compression "+k)}A(v[31]===v[32],"universal relation");rows.push(v);pairs.push([i,j])}
function nullMod(rows,p){let R=rows.map(a=>a.map(x=>((x%p)+p)%p)),piv=[],r=0;for(let j=0;j<43;j++){let k=R.findIndex((a,i)=>i>=r&&a[j]);if(k<0)continue;[R[r],R[k]]=[R[k],R[r]];let iv=1;while(iv*R[r][j]%p!==1)iv++;R[r]=R[r].map(x=>iv*x%p);for(let i=0;i<R.length;i++)if(i!==r&&R[i][j]){let a=R[i][j];R[i]=R[i].map((x,k)=>(x-a*R[r][k]+p*p)%p)}piv.push(j);r++}return {p,rank:r,piv}}
return {n,pairs,rows,denominators:[24*495*1320*59049,...Array(4).fill(48*495*1320*59049),...Array(38).fill(2*1320*1320*59049)],rank_mod:[101,103,107].map(p=>nullMod(rows,p)),universal_duplicate:[31,32],scope:"Exact projected weight4 compression on sampled orbit averages via local kernel and alternating form table. Identity and lower four compressions crosschecked against prior independently generated rational matrices. Rank modulo primes is a lower bound on complex operator rank on full invariant space. Not exact full rank or distance5."}}

const fs=require("fs");
const table=JSON.parse(fs.readFileSync("data/toe_20261128_weight4_local_phase_table.json","utf8"));
const prior=JSON.parse(fs.readFileSync("data/toe_20261128_golay_distance4_explicit.json","utf8"));
console.log(JSON.stringify(rank4Actual(table,prior,10),null,2));
