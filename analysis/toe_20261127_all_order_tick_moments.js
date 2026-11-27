function moment(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},V=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)),P=V.filter(v=>v.find(Boolean)===1),idx=v=>v.reduce((s,x,j)=>s+m(x)*3**j,0),act=V.map(v=>Array.from({length:9},(_,q)=>[m(q%3+v[0])+3*m(Math.floor(q/3)+v[1]),m(v[2]*(q%3)+v[3]*Math.floor(q/3)+2*(v[0]*v[2]+v[1]*v[3]))]));
let counts=[];for(let r=1;r<=20;r++){let d=Array.from({length:3},()=>Array(3).fill(0n));d[0][0]=1n;for(let i=0;i<r;i++){let g=Array.from({length:3},()=>Array(3).fill(0n));for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++)g[m(a+c)][m(b+c*c)]+=d[a][b];d=g}let iso=(d[0][0]-1n)/2n,ref=(d[0][1]+d[0][2])/2n;A(iso+ref===(3n**BigInt(r-1)-1n)/2n,'count');counts.push({r,projectors:String(iso),reflections:String(ref),identity_numerator:String(40n-iso-ref),trace:String(120n*3n**BigInt(r)),trace_squared:String(120n*3n**BigInt(r)+14040n)})}
let tests=[];for(let r of [3,4,5,6]){let patterns=Array.from({length:3**r},(_,i)=>Array.from({length:r},(_,j)=>Math.floor(i/3**j)%3)).filter(a=>!m(a.reduce((s,x)=>s+x,0))),canon=patterns.filter(a=>a.find(Boolean)===1),terms=[];for(let p of P)for(let a of patterns)terms.push(a.map(t=>idx(p.map(x=>t*x))));let pow=Array.from({length:r},(_,i)=>9**i),encode=q=>q.reduce((s,x,i)=>s+x*pow[i],0),N=9**r,cols=r<=4?N:64;
for(let c=0;c<cols;c++){let i=r<=4?c:(c*7919+123)%N,q=pow.map(p=>Math.floor(i/p)%9),M=new Map(),add=(j,e,w)=>{let a=M.get(j)||[0,0];if(e===0)a[0]+=w;else if(e===1)a[1]+=w;else{a[0]-=w;a[1]-=w}M.set(j,a)};
for(let v of terms){let x=v.map((k,j)=>act[k][q[j]]);add(encode(x.map(a=>a[0])),m(x.reduce((s,a)=>s+a[1],0)),1)}
add(i,0,-40+canon.length);
for(let a of canon){let d=m(a.reduce((s,x)=>s+x*x,0)),u=m(a.reduce((s,x,j)=>s+x*(q[j]%3),0)),v=m(a.reduce((s,x,j)=>s+x*Math.floor(q[j]/3),0));if(d){let z=q.map((x,j)=>m(x%3+a[j]*u*d)+3*m(Math.floor(x/3)+a[j]*v*d));add(encode(z),0,-9)}else if(!u&&!v)for(let x=0;x<9;x++){let z=q.map((b,j)=>m(b%3+a[j]*(x%3))+3*m(Math.floor(b/3)+a[j]*Math.floor(x/3)));add(encode(z),0,-9)}}
A([...M.values()].every(a=>!a[0]&&!a[1]),'moment '+r+' '+i)}
tests.push({r,columns:cols,dimension:N,expanded_terms:terms.length})}
return {counts,tests,formula:"3^(r-1) M_r=(40-N_r)I+9 sum_{anisotropic [a] in 1^perp}R_a+81 sum_{isotropic [a] in 1^perp}Pi_a, N_r=(3^(r-1)-1)/2",scope:"All-order algebraic formula from Weyl expansion, exact column verification for r3,4 and samples r5,6; shared-label model not physical dynamics selection."}
}
console.log(JSON.stringify(moment(),null,2));
