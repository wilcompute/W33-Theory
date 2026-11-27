function cube(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},N=8,edges=[];for(let i=0;i<8;i++)for(let d=0;d<3;d++)if(!(i>>d&1))edges.push({i,j:i+(1<<d),d});const powers=edges.map((_,i)=>3**i),states=[],map=new Map(),decode=k=>edges.map((_,i)=>Math.floor(k/powers[i])%3);
for(let k=0;k<3**edges.length;k++){let E=decode(k),D=Array(8).fill(0);edges.forEach(({i,j},l)=>{D[i]-=E[l];D[j]+=E[l]});let q=D.map(m),n=q.every(x=>!x)?0:q[0]===1?q.findIndex((x,i)=>i&&x===2&&q.every((y,j)=>j===0||j===i||y===0)):-1;if(n<0)continue;map.set(n*3**12+k,states.length);states.push({n,k,E})}
A(states.length===1944,'Gauss dimension');
const id=(n,k)=>map.get(n*3**12+k),add=(a,b)=>[a[0]+b[0],a[1]+b[1]],mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],scale=(a,s)=>a.map(x=>x*s),conj=a=>[a[0],-a[1]],ph=t=>[Math.cos(t),Math.sin(t)],zero=()=>[0,0],mm=(M,v)=>M.map(r=>r.reduce((s,x,i)=>add(s,mul(x,v[i])),zero())),adj=M=>M[0].map((_,i)=>M.map(r=>conj(r[i])));
const pauli=[[[[0,0],[1,0]],[[1,0],[0,0]]],[[[0,0],[0,-1]],[[0,1],[0,0]]],[[[1,0],[0,0]],[[0,0],[-1,0]]]],beta=[1,1,-1,-1];
const T=pauli.map(P=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>{let z=i===j?[-beta[i]/2,0]:zero();if((i<2)!==(j<2))z=add(z,mul([0,.5],P[i%2][j%2]));return z}))),Td=T.map(adj);
for(let d=0;d<3;d++)for(let i=0;i<4;i++){let e=Array.from({length:4},(_,j)=>[+(i===j),0]),u=mm(T[d],e),v=mm(T[d],mm(Td[d],u));A(v.every((x,j)=>Math.hypot(x[0]-u[j][0],x[1]-u[j][1])<1e-12),'partial isometry')}
let hops=edges.map(({i,j,d},l)=>states.flatMap((s,k)=>{if(s.n!==i)return [];let e=s.E[l],v=s.k+(m(e-1)-e)*powers[l],b=id(j,v);A(b!==undefined,'Gauss hop');return [[k,b]]}));
let faces=[];for(let i=0;i<8;i++)for(let d=0;d<3;d++)for(let e=d+1;e<3;e++)if(!(i>>d&1)&&!(i>>e&1)){let path=[i,i+(1<<d),i+(1<<d)+(1<<e),i+(1<<e),i],delta=edges.map(({i,j})=>path.slice(0,4).reduce((s,x,k)=>s+(x===i&&path[k+1]===j?1:x===j&&path[k+1]===i?-1:0),0));let f=states.map(s=>{let k=s.E.reduce((t,x,l)=>t+m(x+delta[l])*powers[l],0),b=id(s.n,k);A(b!==undefined,'Gauss face');return b});faces.push(f)}
let psi=states.map(()=>Array.from({length:4},zero));psi[id(0,0)][0]=[1,0];
function hop(l,t){let d=edges[l].d,c=Math.cos(t)-1,z=[0,-Math.sin(t)];for(let [i,j] of hops[l]){let u=psi[i],v=psi[j],tu=mm(T[d],u),tv=mm(Td[d],v),uu=mm(Td[d],tu),vv=mm(T[d],tv);psi[i]=u.map((a,k)=>add(add(a,scale(uu[k],c)),mul(z,tv[k])));psi[j]=v.map((a,k)=>add(add(a,scale(vv[k],c)),mul(z,tu[k])))}}
function mag(f,t){let b=states.map(()=>Array.from({length:4},zero)),coef=[0,1,2].map(r=>[0,1,2].reduce((s,k)=>add(s,scale(ph(-2*t*Math.cos(2*Math.PI*k/3)-2*Math.PI*k*r/3),1/3)),zero()));for(let j=0;j<states.length;j++){let k=j;for(let r=0;r<3;r++){for(let spin=0;spin<4;spin++)b[k][spin]=add(b[k][spin],mul(coef[r],psi[j][spin]));k=f[k]}}psi=b}
let rows=[];for(let t=1;t<=12;t++){for(let i=0;i<states.length;i++)for(let s=0;s<4;s++)psi[i][s]=mul(psi[i][s],ph(-.1*(3.7*beta[s]+.2*states[i].E.filter(Boolean).length)));for(let l=0;l<edges.length;l++)hop(l,.1);for(let f of faces)mag(f,.03);
let P=Array(8).fill(0),el=0,spin=0;for(let i=0;i<states.length;i++)for(let s=0;s<4;s++){let p=psi[i][s][0]**2+psi[i][s][1]**2;P[states[i].n]+=p;el+=p*states[i].E.filter(Boolean).length;spin+=p*beta[s]}
let norm=P.reduce((s,x)=>s+x,0);A(Math.abs(norm-1)<1e-11,'norm');rows.push({step:t,norm,matter:P,electric:el,beta_expectation:spin})}
return {vertices:8,links:12,plaquettes:faces.length,physical_gauge_position_states:states.length,spinorial_dimension:4*states.length,hopping_pairs:hops.map(x=>x.length),rows,scope:'one mobile spinor and static compensating charge, open cube, dimensionless chosen Wilson and gauge parameters; no many-body continuum RG'}
}
console.log(JSON.stringify(cube(),null,2));
