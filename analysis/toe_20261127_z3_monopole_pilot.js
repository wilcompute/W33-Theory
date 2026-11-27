function scan(){
const A=(v,s)=>{if(!v)throw Error(s)},m=x=>(x%3+3)%3,sg=x=>{let r=m(x);return r===2?-1:r},rows=[];
for(let L of [3,4]){
let V=L**4,plus=Array.from({length:V},(_,v)=>Array.from({length:4},(_,d)=>{let a=L**d;return v+(Math.floor(v/a)%L===L-1?1-L:1)*a})),pairs=[],trip=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){pairs.push([a,b]);for(let c=b+1;c<4;c++)trip.push([a,b,c])}
let pi=(v,a,b)=>6*v+pairs.findIndex(p=>p[0]===a&&p[1]===b),pl=[],cu=[],lp=Array.from({length:4*V},()=>[]),pc=Array.from({length:6*V},()=>[]);
for(let v=0;v<V;v++)for(let [a,b] of pairs){let p=pl.length,ls=[[4*v+a,1],[4*plus[v][a]+b,1],[4*plus[v][b]+a,-1],[4*v+b,-1]];pl.push(ls);for(let [l,s] of ls)lp[l].push([p,s])}
for(let v=0;v<V;v++)for(let [a,b,c] of trip){let k=cu.length,ps=[[pi(plus[v][a],b,c),1],[pi(v,b,c),-1],[pi(plus[v][b],a,c),-1],[pi(v,a,c),1],[pi(plus[v][c],a,b),1],[pi(v,a,b),-1]];cu.push(ps);for(let [p,s] of ps)pc[p].push([k,s])}
let seed=177+L,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
for(let mu of [0,1])for(let beta of [.15,.35,.45,.65]){
let E=new Int8Array(4*V),F=new Int8Array(6*V),J=new Int8Array(4*V);for(let l=0;l<E.length;l++)E[l]=Math.floor(rng()*3);
for(let p=0;p<F.length;p++)F[p]=sg(pl[p].reduce((s,[l,z])=>s+z*E[l],0));for(let c=0;c<J.length;c++){let x=cu[c].reduce((s,[p,z])=>s+z*F[p],0);A(x%3===0,'Bianchi');J[c]=x/3}
let tmp=new Int8Array(J.length),touched=new Int32Array(24),stamp=new Int32Array(J.length),serial=0,accepted=0,trials=0,samples=[],changes=new Int8Array(6);
for(let sweep=0;sweep<200;sweep++){
for(let l=0;l<E.length;l++){let d=rng()<.5?1:-1,ds=0,nt=0,k=0;serial++;for(let [p,s] of lp[l]){let f=sg(F[p]+s*d),df=f-F[p];changes[k++]=f;ds+=1.5*beta*(+(f!==0)-+(F[p]!==0));for(let [c,z] of pc[p]){if(stamp[c]!==serial){stamp[c]=serial;tmp[c]=0;touched[nt++]=c}tmp[c]+=z*df}}
for(let i=0;i<nt;i++){let c=touched[i];A(tmp[c]%3===0,'local Bianchi');let v=J[c]+tmp[c]/3;ds+=mu*(v*v-J[c]*J[c])}
trials++;if(ds<=0||rng()<Math.exp(-ds)){accepted++;E[l]=m(E[l]+d);k=0;for(let [p] of lp[l])F[p]=changes[k++];for(let i=0;i<nt;i++){let c=touched[i];J[c]+=tmp[c]/3}}}
if(sweep%50===0){A(F.every((x,i)=>x===sg(pl[i].reduce((s,[l,z])=>s+z*E[l],0))),'flux');A(J.every((x,i)=>3*x===cu[i].reduce((s,[p,z])=>s+z*F[p],0)),'current')}
if(sweep>=80&&sweep%4===0){let nf=F.filter(Boolean).length,nj=J.reduce((s,x)=>s+x*x,0),R=0,I=0;for(let v=0;v<V;v+=L){let j=0;for(let t=0;t<L;t++)j+=E[4*(v+t)];j=m(j);R+=j===0?1:-.5;I+=j===1?Math.sqrt(3)/2:j===2?-Math.sqrt(3)/2:0}R/=V/L;I/=V/L;let mag=Math.hypot(R,I);samples.push({S:1.5*beta*nf+mu*nj,vortex:nf/F.length,monopole:nj/J.length,polyakov:mag,angular:mag?(R**3-3*R*I**2)/mag**3:0})}
}
let mean=k=>samples.reduce((s,x)=>s+x[k],0)/samples.length,avg=mean('S'),chi=samples.reduce((s,x)=>s+(x.S-avg)**2,0)/samples.length/V;
rows.push({L,beta,mu,samples:samples.length,acceptance:accepted/trials,vortex:mean('vortex'),monopole:mean('monopole'),polyakov:mean('polyakov'),angular3:mean('angular'),action_susceptibility:chi})
}}
return {rows,scope:'pilot L3/L4, 80 thermal sweeps+120 measured, 30 correlated samples, one hot start per point, not adequate phase identification'}
}
console.log(JSON.stringify(scan(),null,2));
