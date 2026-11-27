function scanClock(){
const A=(v,s)=>{if(!v)throw Error(s)},m=x=>(x%3+3)%3,sg=x=>{let r=m(x);return r===2?-1:r},rows=[];
for(let L of [4,6]){
let T=2*L,V=T*L**3,plus=Array.from({length:V},(_,v)=>Array.from({length:4},(_,d)=>{let a=d===0?1:T*L**(d-1),len=d===0?T:L;return v+(Math.floor(v/a)%len===len-1?1-len:1)*a})),pairs=[],trip=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){pairs.push([a,b]);for(let c=b+1;c<4;c++)trip.push([a,b,c])}
let pi=(v,a,b)=>6*v+pairs.findIndex(p=>p[0]===a&&p[1]===b),pl=[],cu=[],lp=Array.from({length:4*V},()=>[]),pc=Array.from({length:6*V},()=>[]);
for(let v=0;v<V;v++)for(let [a,b] of pairs){let p=pl.length,ls=[[4*v+a,1],[4*plus[v][a]+b,1],[4*plus[v][b]+a,-1],[4*v+b,-1]];pl.push(ls);for(let [l,s] of ls)lp[l].push([p,s])}
for(let v=0;v<V;v++)for(let [a,b,c] of trip){let k=cu.length,ps=[[pi(plus[v][a],b,c),1],[pi(v,b,c),-1],[pi(plus[v][b],a,c),-1],[pi(v,a,c),1],[pi(plus[v][c],a,b),1],[pi(v,a,b),-1]];cu.push(ps);for(let [p,s] of ps)pc[p].push([k,s])}
let seed=177+L,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
for(let [n,beta,cold] of (L===4?[[4,.35,false],[4,.45,false],[6,.35,false],[6,.45,false],[8,.35,false],[8,.45,false],[6,.4,false],[6,.4,true]]:[[6,.4,false],[6,.4,true]])){let mu=n*.15796197116476024;
let E=new Int8Array(4*V),F=new Int8Array(6*V),J=new Int8Array(4*V);for(let l=0;l<E.length;l++)E[l]=cold?0:Math.floor(rng()*3);
for(let p=0;p<F.length;p++)F[p]=sg(pl[p].reduce((s,[l,z])=>s+z*E[l],0));for(let c=0;c<J.length;c++){let x=cu[c].reduce((s,[p,z])=>s+z*F[p],0);A(x%3===0,'Bianchi');J[c]=x/3}
let tmp=new Int8Array(J.length),touched=new Int32Array(24),stamp=new Int32Array(J.length),serial=0,accepted=0,trials=0,samples=[],changes=new Int8Array(6);
for(let sweep=0;sweep<660;sweep++){
for(let l=0;l<E.length;l++){let d=rng()<.5?1:-1,ds=0,nt=0,k=0;serial++;for(let [p,s] of lp[l]){let f=sg(F[p]+s*d),df=f-F[p];changes[k++]=f;ds+=1.5*beta*(+(f!==0)-+(F[p]!==0));for(let [c,z] of pc[p]){if(stamp[c]!==serial){stamp[c]=serial;tmp[c]=0;touched[nt++]=c}tmp[c]+=z*df}}
for(let i=0;i<nt;i++){let c=touched[i];A(tmp[c]%3===0,'local Bianchi');let v=J[c]+tmp[c]/3;ds+=mu*(v*v-J[c]*J[c])}
trials++;if(ds<=0||rng()<Math.exp(-ds)){accepted++;E[l]=m(E[l]+d);k=0;for(let [p] of lp[l])F[p]=changes[k++];for(let i=0;i<nt;i++){let c=touched[i];J[c]+=tmp[c]/3}}}
if(sweep%50===0){A(F.every((x,i)=>x===sg(pl[i].reduce((s,[l,z])=>s+z*E[l],0))),'flux');A(J.every((x,i)=>3*x===cu[i].reduce((s,[p,z])=>s+z*F[p],0)),'current')}
if(sweep>=180&&sweep%4===0){
let nf=F.filter(Boolean).length,nj=J.reduce((s,x)=>s+x*x,0),corr=[];
for(let mode of [1,2]){
let R=new Float64Array(T),I=new Float64Array(T);
for(let v=0;v<V;v++){let x=Math.floor(v/T)%L,t=v%T,phi=2*Math.PI*mode*x/L,f=F[pi(v,1,2)];R[t]+=f*Math.cos(phi);I[t]+=f*Math.sin(phi)}
let C=Array.from({length:T/2+1},(_,dt)=>R.reduce((s,x,t)=>s+x*R[(t+dt)%T]+I[t]*I[(t+dt)%T],0)/V);corr.push(C)}
let twistDelta=0,delta=new Map();for(let v=0;v<V;v++){let x=Math.floor(v/T)%L,y=Math.floor(v/(T*L))%L;if(x||y)continue;let p=pi(v,1,2),f=sg(F[p]+1),df=f-F[p];twistDelta+=1.5*beta*(+(f!==0)-+(F[p]!==0));for(let [c,z] of pc[p])delta.set(c,(delta.get(c)||0)+z*df)}for(let [c,d] of delta){A(d%3===0,'closed twist');twistDelta+=mu*((J[c]+d/3)**2-J[c]**2)}samples.push({vortex:nf/F.length,monopole:nj/J.length,corr,twistDelta})
}}
let mean=k=>samples.reduce((s,x)=>s+x[k],0)/samples.length;
let correlations=[1,2].map((mode,i)=>{let C=Array.from({length:T/2+1},(_,dt)=>samples.reduce((s,x)=>s+x.corr[i][dt],0)/samples.length);
let blocks=Array.from({length:12},(_,j)=>Array.from({length:C.length},(_,dt)=>samples.slice(j*10,j*10+10).reduce((s,x)=>s+x.corr[i][dt],0)/10));
let se=C.map((x,dt)=>Math.sqrt(blocks.reduce((s,b)=>s+(b[dt]-x)**2,0)/132));
let E0=2*Math.asinh(Math.sin(Math.PI*mode/L)),masslessRatio=Array.from({length:C.length},(_,dt)=>Math.cosh(E0*(T/2-dt))/Math.cosh(E0*T/2));
let fit=c=>{let D=Array.from({length:2},(_,k)=>c.reduce((s,x,j)=>s+x*Math.cos(2*Math.PI*k*j/T)*(j===0||j===T/2?1:2),0)),e2=4*Math.sin(Math.PI/T)**2*D[1]/(D[0]-D[1]);return {E:e2>0?2*Math.asinh(Math.sqrt(e2)/2):null,lattice_mass_squared:e2-4*Math.sin(Math.PI*mode/L)**2}};let full=fit(C),jk=blocks.map(b=>fit(C.map((x,j)=>(12*x-b[j])/11)).lattice_mass_squared),jm=jk.reduce((a,b)=>a+b,0)/12;return {mode,frequency_fit:full,jackknife_mass_squared_se:Math.sqrt(11/12*jk.reduce((s,x)=>s+(x-jm)**2,0)),correlation:C,block_se:se,normalized:C.map(x=>x/C[0]),free_massless_benchmark:masslessRatio,free_massless_energy:E0}});
let ds=samples.map(x=>x.twistDelta),min=Math.min(...ds),rw=ds.map(x=>Math.exp(min-x)),sum=rw.reduce((a,b)=>a+b,0),ess=sum*sum/rw.reduce((a,b)=>a+b*b,0);let a=samples.map(x=>x.monopole),avg=mean('monopole'),var0=a.reduce((s,x)=>s+(x-avg)**2,0),ac=Array.from({length:15},(_,i)=>a.slice(i+1).reduce((s,x,j)=>s+(x-avg)*(a[j]-avg),0)/var0),tau=.5;for(let x of ac){if(x<=0)break;tau+=x}rows.push({L,T,n,beta,mu,cold,twist:{free_energy_one_sided:min-Math.log(sum/ds.length),importance_ess:ess,min_delta:min},monopole_autocorrelation:ac,monopole_tau_sample_units:tau,samples:samples.length,acceptance:accepted/trials,vortex:mean('vortex'),monopole:mean('monopole'),correlations})

}}
return {rows,scope:'Scan of repeated clock Z3 gauge model, 180 burn-in and 480 measured sweeps, 120 correlated samples per chain, 12 blocks. Frequency-ratio single-pole diagnostic, jackknife error descriptive; one-sided discrete twisted-flux reweighting is not continuous helicity modulus and fails if ESS low. No controlled continuum claim.'}
}
console.log(JSON.stringify(scanClock(),null,2));
