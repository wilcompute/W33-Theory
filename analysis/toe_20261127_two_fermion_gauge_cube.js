function twoFermions(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},edges=[];
for(let i=0;i<8;i++)for(let d=0;d<3;d++)if(!(i>>d&1))edges.push({i,j:i+(1<<d),d});
let tree=[],free=[],parent=Array(8).fill(-1),pe=Array(8).fill(-1);
for(let j=1;j<8;j++){let d=0;while(!(j>>d&1))d++;let i=j-(1<<d),l=edges.findIndex(e=>e.i===i&&e.j===j);tree.push(l);parent[j]=i;pe[j]=l}for(let l=0;l<12;l++)if(!tree.includes(l))free.push(l);
const F=243,pow=free.map((_,i)=>3**i),field=(n1,n2,k)=>{let E=Array(12).fill(0),D=Array(8).fill(0),q=Array(8).fill(0);q[0]=q[7]=1;q[n1]--;q[n2]--;for(let l=0;l<5;l++){let e=edges[free[l]],v=Math.floor(k/pow[l])%3;E[free[l]]=v;D[e.i]-=v;D[e.j]+=v}
for(let j=7;j>0;j--){let v=m(q[j]-D[j]);E[pe[j]]=v;D[j]+=v;D[parent[j]]-=v}A(D.every((x,i)=>m(x-q[i])===0),'Gauss');return E};
let pos=new Map();for(let i=0;i<8;i++)for(let j=i;j<8;j++)pos.set(8*i+j,Array.from({length:F},(_,k)=>field(i,j,k).filter(Boolean).length));
let pairs=[],pid=Array.from({length:32},()=>Array(32).fill(-1));for(let i=0;i<32;i++)for(let j=i+1;j<32;j++){pid[i][j]=pid[j][i]=pairs.length;pairs.push([i,j])}let N=pairs.length*F,R=new Float64Array(N),I=new Float64Array(N);
A(N===120528,'dimension');R[pid[0][28]*F]=1;
let beta=[1,1,-1,-1],pauli=[[[[0,0],[1,0]],[[1,0],[0,0]]],[[[0,0],[0,-1]],[[0,1],[0,0]]],[[[1,0],[0,0]],[[0,0],[-1,0]]]];
let gates=[];
for(let l=0;l<12;l++){let {i,j,d}=edges[l];for(let a=0;a<4;a++)for(let b=0;b<4;b++){let z=[0,0];if(a===b)z=[-beta[a]/2,0];if((a<2)!==(b<2)){let p=pauli[d][b%2][a%2];z=[-p[1]/2,p[0]/2]}if(!z[0]&&!z[1])continue;let u=4*i+a,v=4*j+b,ps=[];for(let w=0;w<32;w++)if(w!==u&&w!==v){let sign=(w>Math.min(u,v)&&w<Math.max(u,v))?-1:1;ps.push([pid[u][w],pid[v][w],sign])}gates.push({l,z,ps})}}
let shift=(k,l,step)=>{let n=free.indexOf(l);if(n<0)return k;let p=pow[n],x=Math.floor(k/p)%3;return k+(m(x+step)-x)*p};
let faceMaps=[];
for(let i=0;i<8;i++)for(let d=0;d<3;d++)for(let e=d+1;e<3;e++)if(!(i>>d&1)&&!(i>>e&1)){let path=[i,i+(1<<d),i+(1<<d)+(1<<e),i+(1<<e),i],del=edges.map(({i,j})=>path.slice(0,4).reduce((s,x,k)=>s+(x===i&&path[k+1]===j?1:x===j&&path[k+1]===i?-1:0),0)),map=Array.from({length:F},(_,k)=>free.reduce((s,l)=>shift(s,l,del[l]),k));A(map.every((j,k)=>map[map[j]]===k),'cycle');faceMaps.push(map)}
// independently check every local charge move and every flux-coordinate circulation on a sample of fields
for(let l=0;l<12;l++){let {i,j}=edges[l];for(let w=0;w<8;w++)for(let k=0;k<F;k++){let a=field(i,w,k),b=field(j,w,shift(k,l,-1));A(a.every((x,h)=>m(x-(h===l?1:0))===b[h]),'physical link update')}}
const phase=(idx,t)=>{let c=Math.cos(t),s=Math.sin(t),r=R[idx],i=I[idx];R[idx]=c*r-s*i;I[idx]=s*r+c*i};
function hop(g,t){let [zr,zi]=g.z,n=Math.hypot(zr,zi),c=Math.cos(t*n),s=Math.sin(t*n)/n;for(let [p,q,sg] of g.ps){let br=sg*zr*s,bi=sg*zi*s;for(let k=0;k<F;k++){let a=p*F+k,b=q*F+shift(k,g.l,-1),ur=R[a],ui=I[a],vr=R[b],vi=I[b];R[a]=c*ur-bi*vr+br*vi;I[a]=c*ui-bi*vi-br*vr;R[b]=c*vr+bi*ur+br*ui;I[b]=c*vi+bi*ui-br*ur}}}
function magnetic(map,t){let cr=[],ci=[];for(let r=0;r<3;r++){cr[r]=0;ci[r]=0;for(let k=0;k<3;k++){let a=-2*t*Math.cos(2*Math.PI*k/3)-2*Math.PI*k*r/3;cr[r]+=Math.cos(a)/3;ci[r]+=Math.sin(a)/3}}let nr=new Float64Array(N),ni=new Float64Array(N);for(let p=0;p<pairs.length;p++)for(let k=0;k<F;k++){let j=k,a=p*F+k;for(let r=0;r<3;r++){let b=p*F+j;nr[b]+=cr[r]*R[a]-ci[r]*I[a];ni[b]+=cr[r]*I[a]+ci[r]*R[a];j=map[j]}}R=nr;I=ni}
let rows=[];for(let t=1;t<=6;t++){for(let p=0;p<pairs.length;p++){let [a,b]=pairs[p],x=a>>2,y=b>>2,E=pos.get(8*x+y);for(let k=0;k<F;k++)phase(p*F+k,-.1*(3.7*(beta[a%4]+beta[b%4])+.2*E[k]))}for(let g of gates)hop(g,.1);for(let f of faceMaps)magnetic(f,.03);
let norm=0,occ=Array(8).fill(0),electric=0,double=0,dist=0;for(let p=0;p<pairs.length;p++){let [a,b]=pairs[p],x=a>>2,y=b>>2,E=pos.get(8*x+y),d=(x^y).toString(2).replace(/0/g,'').length;for(let k=0;k<F;k++){let j=p*F+k,v=R[j]**2+I[j]**2;norm+=v;occ[x]+=v;occ[y]+=v;electric+=v*E[k];if(x===y)double+=v;dist+=v*d}}A(Math.abs(norm-1)<1e-10,'norm');rows.push({step:t,norm,occupation:occ,electric,double_occupation:double,pair_distance:dist})}
return {dimension:N,orbitals:32,fermions:2,flux_states_per_pair:F,local_hopping_gates:gates.length,plaquettes:faceMaps.length,verified_charge_transitions:12*8*F,rows,scope:'two identical fermions in first-quantized fixed-number Fock sector; Wilson spinor, dynamical Z3 links, open cube; first-order orbital Trotter splitting'}
}
console.log(JSON.stringify(twoFermions(),null,2));
