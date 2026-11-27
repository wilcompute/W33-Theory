function verify(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)};
 // V tensor V multiplicity coordinates: mean s, difference r. commuting relative X and Z.
 let rel=[];for(let x=0;x<3;x++)for(let y=0;y<3;y++){let s=m(2*(x+y)),r=m(y-x);A(m(s+r)===x&&m(s-r)===y,'inverse');A(m(2*(x+1+y-1))===s&&m((y-1)-(x+1))===m(r+1),'relative X');rel.push([x,y,s,r])}
 let F=[];for(let p=0;p<3;p++)for(let q=0;q<3;q++){let mat=[];for(let r=0;r<3;r++){let row=[];for(let s=0;s<3;s++){let z=[0,0,0];for(let x=0;x<3;x++)for(let y=0;y<3;y++){let z1=m(q-x-y);if(m(y-x)!==r||m(z1-y)!==s)continue;z[m(p*(y-x))]++}if(z.reduce((a,b)=>a+b,0))A(z[m(p*r)]===3&&s===m(q+r),'recoupling');row.push(z.reduce((a,b)=>a+b,0)?m(p*r):null)}mat.push(row)}F.push({p,q,matrix_exponents:mat})}
 // exact physical one-particle gauge sector on open square, oriented cyclic links.
 // charges: n_i + incoming E - outgoing E, external static charge at vertex0.
 const states=[];for(let n=0;n<4;n++)for(let j=0;j<81;j++){let E=Array.from({length:4},(_,i)=>Math.floor(j/3**i)%3);if(E.every((e,i)=>m(+(i===n)+E[(i+3)%4]-e)===+(i===0)))states.push({n,E})}
 A(states.length===12,'physical sector');
 const id=(n,E)=>states.findIndex(s=>s.n===n&&s.E.join()===E.join()),N=states.length;
 let pairs=[];for(let i=0;i<4;i++){let p=[];for(let j=0;j<N;j++){let {n,E}=states[j];if(n!==i)continue;let R=E.slice();R[i]=m(R[i]-1);let k=id((i+1)%4,R);A(k>=0,'gauge hop');p.push([j,k])}pairs.push(p)}
 let loops=[];for(let j=0;j<N;j++){let {n,E}=states[j];loops.push(id(n,E.map(x=>m(x+1))));A(loops[j]>=0,'plaquette')}
 const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],ph=x=>[Math.cos(x),Math.sin(x)],scale=(a,k)=>a.map(x=>x*k);
 let a=Array.from({length:N},()=>[0,0]);a[id(0,[0,0,0,0])]=[1,0];
 function hop(i,t){for(let [j,k] of pairs[i]){let u=a[j],v=a[k];a[j]=add(scale(u,Math.cos(t)),mul(v,[0,-Math.sin(t)]));a[k]=add(scale(v,Math.cos(t)),mul(u,[0,-Math.sin(t)]))}}
 function magnetic(t){let b=Array.from({length:N},()=>[0,0]),coef=Array.from({length:3},(_,r)=>[0,1,2].reduce((s,k)=>add(s,scale(ph(-2*t*Math.cos(2*Math.PI*k/3)-2*Math.PI*k*r/3),1/3)),[0,0]));for(let j=0;j<N;j++){let k=j;for(let r=0;r<3;r++){b[k]=add(b[k],mul(coef[r],a[j]));k=loops[k]}}a=b}
 let rows=[];for(let step=1;step<=10;step++){for(let i=0;i<N;i++)a[i]=mul(a[i],ph(-.2*states[i].E.filter(Boolean).length));for(let i of [0,2,1,3])hop(i,.15);magnetic(.12);let P=[0,0,0,0],electric=0;for(let i=0;i<N;i++){let v=a[i][0]**2+a[i][1]**2;P[states[i].n]+=v;electric+=v*states[i].E.filter(Boolean).length}A(Math.abs(P.reduce((s,v)=>s+v,0)-1)<1e-12,'unitarity');rows.push({step,matter_position:P,electric})}
 return {multiplicity:{relative_coordinates:rel,recoupling:F,relative_Weyl:'X1 X2^-1, Z1^-1 Z2'},gauge_plaquette:{physical_dimension:N,local_pairs:pairs,magnetic_cycle:loops,rows,scope:'2D open plaquette with static compensating charge; exact local gates embed on 3D cubic lattice; not interacting continuum simulation'}}
}
console.log(JSON.stringify(verify(),null,2));
