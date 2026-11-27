function bridge(){
const A=(x,s)=>{if(!x)throw Error(s)},m=x=>(x%3+3)%3,sg=x=>m(x)===2?-1:m(x),rows=[];
for(let L of [2,3]){let T=2*L,V=T*L**3,plus=Array.from({length:V},(_,v)=>Array.from({length:4},(_,d)=>{let a=d===0?1:T*L**(d-1),len=d===0?T:L;return v+(Math.floor(v/a)%len===len-1?1-len:1)*a})),pairs=[],trip=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){pairs.push([a,b]);for(let c=b+1;c<4;c++)trip.push([a,b,c])}
let pi=(v,a,b)=>6*v+pairs.findIndex(p=>p[0]===a&&p[1]===b),pl=[],cu=[],lp=Array.from({length:4*V},()=>[]),pc=Array.from({length:6*V},()=>[]),B=new Int8Array(6*V);
for(let v=0;v<V;v++)for(let [a,b] of pairs){let p=pl.length,ls=[[4*v+a,1],[4*plus[v][a]+b,1],[4*plus[v][b]+a,-1],[4*v+b,-1]];pl.push(ls);for(let [l,s] of ls)lp[l].push([p,s]);if(a===1&&b===2&&Math.floor(v/T)%L===0&&Math.floor(v/(T*L))%L===0)B[p]=1}
for(let v=0;v<V;v++)for(let [a,b,c] of trip){let k=cu.length,ps=[[pi(plus[v][a],b,c),1],[pi(v,b,c),-1],[pi(plus[v][b],a,c),-1],[pi(v,a,c),1],[pi(plus[v][c],a,b),1],[pi(v,a,b),-1]];cu.push(ps);for(let [p,s] of ps)pc[p].push([k,s]);A(ps.reduce((s,[p,z])=>s+z*B[p],0)===0,"closed")}
for(let reverse of [false,true]){let seed=193+L*79+19*reverse,rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},E=Int8Array.from({length:4*V},()=>reverse?0:Math.floor(rng()*3)),beta=.4,mu=6*.15796197116476024,stages=[];
for(let j=0;j<=4;j++){let t=(reverse?4-j:j)/4,F=[0,1].map(h=>Int8Array.from(pl,(ls,p)=>sg(h*B[p]+ls.reduce((s,[l,z])=>s+z*E[l],0)))),J=F.map(f=>Int8Array.from(cu,ps=>ps.reduce((s,[p,z])=>s+z*f[p],0)/3)),tmp=[new Int8Array(J[0].length),new Int8Array(J[0].length)],stamp=new Int32Array(J[0].length),touched=new Int32Array(24),change=[new Int8Array(6),new Int8Array(6)],serial=0,samples=[];
let energy=h=>1.5*beta*F[h].filter(Boolean).length+mu*J[h].reduce((s,x)=>s+x*x,0);
for(let sweep=0;sweep<160;sweep++){for(let l=0;l<E.length;l++){let d=rng()<.5?1:-1,ds=[0,0],nt=0,k=0;serial++;
for(let [p,s] of lp[l]){for(let h=0;h<2;h++){let f=sg(F[h][p]+s*d);change[h][k]=f;ds[h]+=1.5*beta*(+(f!==0)-+(F[h][p]!==0))}for(let [c,z] of pc[p]){if(stamp[c]!==serial){stamp[c]=serial;tmp[0][c]=tmp[1][c]=0;touched[nt++]=c}for(let h=0;h<2;h++)tmp[h][c]+=z*(change[h][k]-F[h][p])}k++}
for(let i=0;i<nt;i++)for(let h=0;h<2;h++){let c=touched[i];A(tmp[h][c]%3===0,"Bianchi");let v=J[h][c]+tmp[h][c]/3;ds[h]+=mu*(v*v-J[h][c]*J[h][c])}let de=(1-t)*ds[0]+t*ds[1];if(de<=0||rng()<Math.exp(-de)){E[l]=m(E[l]+d);k=0;for(let [p] of lp[l]){for(let h=0;h<2;h++)F[h][p]=change[h][k];k++}for(let i=0;i<nt;i++)for(let h=0;h<2;h++)J[h][touched[i]]+=tmp[h][touched[i]]/3}}
if(sweep%40===0)for(let h=0;h<2;h++){A(F[h].every((f,p)=>f===sg(h*B[p]+pl[p].reduce((s,[l,z])=>s+z*E[l],0))),"flux");A(J[h].every((x,c)=>3*x===cu[c].reduce((s,[p,z])=>s+z*F[h][p],0)),"current")}
if(sweep>=60&&sweep%2===0)samples.push(energy(1)-energy(0))}
let mean=samples.reduce((a,b)=>a+b,0)/50,blocks=Array.from({length:5},(_,i)=>samples.slice(i*10,i*10+10).reduce((a,b)=>a+b,0)/10),se=Math.sqrt(blocks.reduce((s,x)=>s+(x-mean)**2,0)/20);stages.push({t,mean,se})}
stages.sort((a,b)=>a.t-b.t);rows.push({L,reverse,simpson:stages.reduce((s,a,i)=>s+[1,4,2,4,1][i]*a.mean,0)/12,coarse_simpson:(stages[0].mean+4*stages[2].mean+stages[4].mean)/6,stages})
}}
return {rows,scope:"Linear bridge of two full actions, derivative exact; short sequential chains 60 burn/100 measured sweeps, 50 measurements per stage, 5 stage points, forward/reverse starts. Small-volume pilot, not equilibrium proof or photon mass."}
}
console.log(JSON.stringify(bridge(),null,2));
