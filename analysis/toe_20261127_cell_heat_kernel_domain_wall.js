function cell(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},V=Array.from({length:27},(_,i)=>[i%3,Math.floor(i/3)%3,Math.floor(i/9)]),hist=[0,0,0];for(let a of V)for(let b of V)hist[m(a[0]*b[1]-a[1]*b[0])]++;
A(hist.join()==="297,216,216",'commutator');let rows=[];
for(let t of [.1,1,4])for(let g=0;g<=8;g++){let f=[1,0,0];for(let i=0;i<g;i++)f=f.map((_,j)=>f.reduce((s,x,k)=>s+x*hist[m(j-k)]/729,0));let a=Math.exp(-t),Z=1-a+27*a*f[0],pred=1+(8+2*9**(1-g))*a;A(Math.abs(Z-pred)<1e-12,'genus');rows.push({t,g,abelian_Z:1+2*a,H27_Z:Z})}
let moves=[];for(let t of [.1,.5,2]){let w=x=>1+2*Math.exp(-x),f=(x,k)=>1+Math.exp(-x)*(k===0?2:-1);let conv=(a,b)=>Array.from({length:3},(_,k)=>a.reduce((s,x,j)=>s+x*b[m(k-j)]/3,0)),u=Array.from({length:3},(_,k)=>f(t,k)),v=Array.from({length:3},(_,k)=>f(t/3,k)),r=conv(conv(v,v),v);A(r.every((x,i)=>Math.abs(x-u[i])<1e-12),'1-3');moves.push({t,original:u,refined:r,unnormalized_fixed_face_weight_change:conv(conv(u,u),u).map((x,i)=>x-u[i])})}
return {H27_commutator_counts:hist,rows,moves,scope:"Exact two-dimensional heat-kernel lattice gauge partition on connected orientable closed surfaces, normalized Haar measure. 1-3 area subdivision and 2-2 fixed total area follow central convolution. No geometry entropy or genus-changing amplitudes derived. For abelian Z3 normalized partition independent of genus; H27 distinguishes genus but favors sphere in equal prior comparison."}
}
function wall(){
const A=(v,s)=>{if(!v)throw Error(s)},rows=[];
function minSing(N,m){let H=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>i===j?m*m+(i===N-1?0:1):Math.abs(i-j)===1?-m:0)); // B lower shift, B^T B
for(let s=0;s<80;s++){let max=0;for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){let x=H[i][j];max=Math.max(max,Math.abs(x));if(Math.abs(x)<1e-15)continue;let t=.5*Math.atan2(2*x,H[j][j]-H[i][i]),c=Math.cos(t),d=Math.sin(t),a=H[i][i],b=H[j][j];H[i][i]=c*c*a-2*c*d*x+d*d*b;H[j][j]=d*d*a+2*c*d*x+c*c*b;H[i][j]=H[j][i]=0;for(let k=0;k<N;k++)if(k!==i&&k!==j){let u=H[k][i],v=H[k][j];H[k][i]=H[i][k]=c*u-d*v;H[k][j]=H[j][k]=d*u+c*v}}if(max<1e-13)break}return Math.sqrt(Math.max(0,Math.min(...H.map((r,i)=>r[i]))))}
for(let N of [4,8,12,16])for(let m of [.5,2.5,4.5,6.5]){let s=minSing(N,m),bound=m<1?m**N*Math.sqrt((1-m*m)/(1-m**(2*N))):m-1;A(m<1?s<=bound+1e-8:s>=bound-1e-8,'wall bound');rows.push({N,m,momentum_pi_coordinates:(m-.5)/2,min_singular:s,bound})}
let anomaly=[];let fam=[{name:"Q",n:6,Y:1},{name:"uc",n:3,Y:-4},{name:"dc",n:3,Y:2},{name:"L",n:2,Y:-3},{name:"ec",n:1,Y:6},{name:"nuc",n:1,Y:0}];anomaly=[fam.reduce((s,x)=>s+x.n*x.Y,0),fam.reduce((s,x)=>s+x.n*x.Y**3,0),2*1-4+2,3*1-3];A(anomaly.every(x=>!x),'SM anomaly');
return {rows,anomaly,SU2_doublets:4,scope:"Supplied 4D spatial Wilson/domain-wall benchmark. H=sin k·sigma tau_z plus SSH offdiagonal B=m(k)I-shift. Both boundaries carry opposite chirality; only k=0 has m<1 for m0=.5. Does not gap mirror, derive extra dimension or gravity. SM anomaly check per 16 including neutral singlet, not proof lattice regulator."}
}
console.log(JSON.stringify({cells:cell(),wall:wall()},null,2));
