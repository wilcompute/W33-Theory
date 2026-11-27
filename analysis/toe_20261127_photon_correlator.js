function photon(){
const m=x=>(x%3+3)%3,sg=x=>{let r=m(x);return r===2?-1:r},A=(v,s)=>{if(!v)throw Error(s)},rows=[];
for(let L of [4,6]){
let V=L**4,N=L**3,plus=Array.from({length:V},(_,v)=>Array.from({length:4},(_,d)=>{let a=L**d;return v+(Math.floor(v/a)%L===L-1?1-L:1)*a})),pairs=[],trip=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){pairs.push([a,b]);for(let c=b+1;c<4;c++)trip.push([a,b,c])}
let pi=(v,a,b)=>6*v+pairs.findIndex(p=>p[0]===a&&p[1]===b),pl=[],cu=[],lp=Array.from({length:4*V},()=>[]),pc=Array.from({length:6*V},()=>[]);
for(let v=0;v<V;v++)for(let [a,b] of pairs){let p=pl.length,ls=[[4*v+a,1],[4*plus[v][a]+b,1],[4*plus[v][b]+a,-1],[4*v+b,-1]];pl.push(ls);for(let [l,s] of ls)lp[l].push([p,s])}
for(let v=0;v<V;v++)for(let [a,b,c] of trip){let k=cu.length,ps=[[pi(plus[v][a],b,c),1],[pi(v,b,c),-1],[pi(plus[v][b],a,c),-1],[pi(v,a,c),1],[pi(plus[v][c],a,b),1],[pi(v,a,b),-1]];cu.push(ps);for(let [p,s] of ps)pc[p].push([k,s])}
let links=lp.map(l=>({p:l.map(x=>x[0]),s:l.map(x=>x[1]),c:l.map(([p])=>pc[p].map(x=>x[0])),z:l.map(([p])=>pc[p].map(x=>x[1]))})),cos=Array.from({length:L},(_,x)=>Math.cos(2*Math.PI*x/L)),sin=Array.from({length:L},(_,x)=>Math.sin(2*Math.PI*x/L));
for(let [beta,mu] of [[.4,0],[.4,1],[.65,1]])for(let hot of [false,true]){
let seed=1234+L*29+Math.round(beta*100)+mu*13+17*hot,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},E=new Int8Array(4*V),F=new Int8Array(6*V),J=new Int8Array(4*V),tmp=new Int8Array(4*V),stamp=new Int32Array(4*V),touched=new Int32Array(24),changes=new Int8Array(6),serial=0,accepted=0,ns=0,sumT=Array(L).fill(0),sumL=Array(L).fill(0),blocks=[],block=[],density=0,vortex=0;
if(hot)for(let i=0;i<E.length;i++)E[i]=Math.floor(rng()*3);
for(let p=0;p<F.length;p++)F[p]=sg(pl[p].reduce((s,[l,z])=>s+z*E[l],0));for(let c=0;c<J.length;c++)J[c]=cu[c].reduce((s,[p,z])=>s+z*F[p],0)/3;
let sweeps=L===6?120:180,thermal=L===6?60:80;
for(let sweep=0;sweep<sweeps;sweep++){
for(let l=0;l<E.length;l++){let d=rng()<.5?1:-1,ds=0,nt=0,k=links[l];serial++;for(let i=0;i<6;i++){let p=k.p[i],f=sg(F[p]+k.s[i]*d),df=f-F[p];changes[i]=f;ds+=1.5*beta*(+(f!==0)-+(F[p]!==0));for(let z=0;z<4;z++){let c=k.c[i][z];if(stamp[c]!==serial){stamp[c]=serial;tmp[c]=0;touched[nt++]=c}tmp[c]+=k.z[i][z]*df}}for(let i=0;i<nt;i++){let c=touched[i],df=tmp[c]/3;A(Number.isInteger(df),'Bianchi');let v=J[c]+df;ds+=mu*(v*v-J[c]*J[c])}if(ds<=0||rng()<Math.exp(-ds)){accepted++;E[l]=m(E[l]+d);for(let i=0;i<6;i++)F[k.p[i]]=changes[i];for(let i=0;i<nt;i++){let c=touched[i];J[c]+=tmp[c]/3}}}
if(sweep===sweeps-1){A(F.every((x,i)=>x===sg(pl[i].reduce((s,[l,z])=>s+z*E[l],0))),'flux rebuild');A(J.every((x,i)=>3*x===cu[i].reduce((s,[p,z])=>s+z*F[p],0)),'current rebuild');for(let j=0;j<4;j++){let plane=0;for(let v=0;v<V;v++)if(Math.floor(v/L**j)%L===0){/* check period below using complementary 3-cycle */} }}
if(sweep>=thermal&&sweep%2===0){ns++;density+=J.reduce((s,x)=>s+x*x,0)/J.length;vortex+=F.filter(Boolean).length/F.length;let R=[Array(L).fill(0),Array(L).fill(0)],I=[Array(L).fill(0),Array(L).fill(0)];for(let v=0;v<V;v++){let t=Math.floor(v/N),x=v%L;for(let j=0;j<2;j++){let f=F[6*v+(j===0?0:3)];R[j][t]+=f*cos[x];I[j][t]+=f*sin[x]}}let cc=[sumT,sumL];let t0=0,t1=0;for(let j=0;j<2;j++)for(let dt=0;dt<L;dt++){let c=0;for(let t=0;t<L;t++){let u=(t+dt)%L;c+=R[j][t]*R[j][u]+I[j][t]*I[j][u]}c/=L*N;cc[j][dt]+=c;if(j===0&&dt===0)t0=c;if(j===0&&dt===1)t1=c}block.push([t0,t1]);if(block.length===5){blocks.push(block);block=[]}}
}
let C=sumT.map(x=>x/ns),D=sumL.map(x=>x/ns),rat=C[1]/C[0],jk=blocks.map((b,i)=>{let a=blocks.filter((_,j)=>j!==i).flat();return a.reduce((s,x)=>s+x[1],0)/a.reduce((s,x)=>s+x[0],0)}),jmean=jk.reduce((s,x)=>s+x,0)/jk.length,jse=Math.sqrt((jk.length-1)/jk.length*jk.reduce((s,x)=>s+(x-jmean)**2,0));let Efree=2*Math.asinh(Math.sin(Math.PI/L)),freeRatio=Math.cosh(Efree*(L/2-1))/Math.cosh(Efree*L/2);
rows.push({L,beta,mu,hot,sweeps,ns,acceptance:accepted/(sweeps*E.length),monopole:density/ns,vortex:vortex/ns,Ctransverse:C,Clongitudinal:D,C1overC0:rat,block_jackknife_se:jse,freePhotonRatio:freeRatio,freePhotonEnergy:Efree})
}}
return {rows,scope:'short hot/cold pilot, projected principal flux correlations; jackknife blocks too short to establish equilibration or massless pole'}
}
console.log(JSON.stringify(photon(),null,2));
