function research(){
const A=(x,m)=>{if(!x)throw Error(m)}, V=(n,p)=>Array.from({length:p**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/p**(n-1-j))%p)), id=(a,p)=>a.reduce((s,x)=>s*p+x,0), dot=(a,b,p)=>a.reduce((s,x,i)=>s+x*b[i],0)%p, hist=a=>{let h={};for(let x of a)h[x]=(h[x]||0)+1;return h}, inter=(a,b)=>a.filter(x=>b.has(x)).length;
function planes(p,n,tetra=false){
 const W=V(2*n,p),q=x=>tetra?dot(x,x,p):dot(x.slice(0,n),x.slice(n),p),bil=(a,b)=>tetra?dot(a,b,p):(dot(a.slice(0,n),b.slice(n),p)+dot(b.slice(0,n),a.slice(n),p))%p;
 const N=W.filter(x=>!q(x));let L=[[0]];
 for(let r=0;r<n;r++){let next=new Map();for(let U of L){let S=new Set(U);for(let b of N){if(S.has(id(b,p))||U.some(a=>bil(W[a],b)))continue;let E=[];for(let a of U)for(let k=0;k<p;k++)E.push(id(W[a].map((x,i)=>(x+k*b[i])%p),p));E.sort((a,b)=>a-b);next.set(E.join(),E)}}L=[...next.values()]}
 let expected=2*Array.from({length:n-1},(_,i)=>p**(i+1)+1).reduce((a,b)=>a*b,1);A(L.length===expected,'plane count');
 let S=L.map(x=>new Set(x)),sign=L.map(x=>(-1)**(n-Math.round(Math.log(inter(x,S[0]))/Math.log(p))));A(sign.reduce((a,b)=>a+b,0)===0,'balance');
 let checks=[];for(let g=1;g<=n+1;g++){let eig=Array.from({length:n},(_,i)=>p**g-p**i).reduce((a,b)=>a*b,1);for(let i=0;i<L.length;i++)A(L.reduce((s,U,j)=>s+sign[j]*inter(U,S[i])**g,0)===sign[i]*eig,'signed Gram');checks.push({g,numerator:eig,denominator:p**(n*g),probability:eig/p**(n*g)})}
 return {summary:{p,n,planes:L.length,null_vectors:N.length,intersection_histogram:hist(L.map(x=>Math.round(Math.log(inter(x,S[0]))/Math.log(p)))),signed_gram:checks},C:L.map(x=>x.map(i=>W[i]))}
}
function gaussian(n,k,p){let a=1n,b=1n;for(let i=0;i<k;i++){a*=BigInt(p)**BigInt(n-i)-1n;b*=BigInt(p)**BigInt(k-i)-1n}return a/b}
function alternating(r,s,p){let t=1n;for(let i=0;i<s;i++)t*=(BigInt(p)**BigInt(2*i+1)-1n)*BigInt(p)**BigInt(2*i);return gaussian(r,2*s,p)*t}
function orbitDims(p,n){let v=[];for(let g=1;g<=n;g++){let d=0n;for(let r=0;r<=n;r++)for(let s=0;s<=Math.floor(r/2);s++)if(r-s<=g)d+=gaussian(n,r,p)*alternating(r,s,p);v.push(d.toString())}let M=2n;for(let i=1;i<n;i++)M*=BigInt(p)**BigInt(i)+1n;A(v.at(-1)===M.toString(),'stable count');return {p,n,dimensions:v,stable:M.toString()}}
function pachner(C){
 const faces=t=>t.map((_,i)=>t.filter((_,j)=>i!==j).join('')).sort(), B=['013','023','123','014','024','124'], left=[faces([0,1,2,3]),faces([0,1,2,4])],right=[faces([0,1,3,4]),faces([0,2,3,4]),faces([1,2,3,4])];
 const build=(F,codes)=>{let out=new Map();function rec(k,d){if(k===F.length){let key=B.map(x=>d[x]).join('');out.set(key,(out.get(key)||0)+1);return}for(let word of codes[k]){if(F[k].some((x,j)=>d[x]!==undefined&&d[x]!==word[j]))continue;let e={...d};F[k].forEach((x,j)=>e[x]=word[j]);rec(k+1,e)}}rec(0,{});return out};
 let l=[],r=[];for(let a of C)for(let b of C){l.push(build(left,[a,b]));for(let c of C)r.push(build(right,[a,b,c]))}
 let maxF=0,eq=0;const norm=x=>[...x.values()].reduce((s,a)=>s+a*a,0);for(let a of l)for(let b of r){let d=0;for(let [k,v] of a)d+=v*(b.get(k)||0);let na=norm(a),nb=norm(b);if(d*d===na*nb)eq++;maxF=Math.max(maxF,d*d/na/nb)}
 return {left_cases:l.length,right_cases:r.length,pairs:l.length*r.length,proportional_pairs:eq,max_squared_overlap:maxF,left_support:hist(l.map(x=>x.size)),right_support:hist(r.map(x=>x.size)),right_multiplicities:hist(r.flatMap(x=>[...x.values()]))}
}
function codes(){
 const C=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>i===j?0:i===0||j===0?1:[1,4].includes((i-j+5)%5)?1:2));
 for(let i=0;i<6;i++)for(let j=0;j<6;j++)A(dot(C[i],C[j],3)===(i===j?2:0),'conference');
 const G=V(6,3).map(x=>x.concat(C[0].map((_,j)=>x.reduce((s,a,i)=>s+a*C[i][j],0)%3))),w=x=>x.filter(Boolean).length,gh=hist(G.map(w));A(JSON.stringify(gh)===JSON.stringify({0:1,6:264,9:440,12:24}),'ternary Golay');
 const mul=(a,b)=>{let z=0;for(let i=0;i<2;i++)if(b>>i&1)z^=a<<i;return z&4?z^7:z},conj=x=>mul(x,x),H=V(3,4).map(([a,b,c])=>[a,b,c,a^b^c,a^mul(2,b)^mul(3,c),a^mul(3,b)^mul(2,c)]);
 A(H.every(x=>H.every(y=>x.reduce((s,a,i)=>s^mul(a,conj(y[i])),0)===0)),'hexacode hermitian');const hh=hist(H.map(w));A(JSON.stringify(hh)===JSON.stringify({0:1,4:45,6:18}),'hex weights');
 const B=[],gen=[0,1,5,6,7,9,11].reduce((s,x)=>s|(1<<x),0),pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
 for(let i=0;i<4096;i++){let a=0;for(let j=0;j<12;j++)if(i>>j&1)a^=gen<<j;B.push(a|((pop(a)%2)<<23))}
 const bh=hist(B.map(pop));A(JSON.stringify(bh)===JSON.stringify({0:1,8:759,12:2576,16:759,24:1}),'binary Golay');
 let odd=0;const oddPer=[];for(let j=0;j<24;j++){let count=0;for(let b of B){let total=0;for(let k=0;k<24;k++){let v=k===0?-3:1,m=k===j?3:1,x=((m-v-2*((b>>k)&1))%4+4)%4===0?m:-m;A(((x-v-2*((b>>k)&1))%4+4)%4===0,'odd residue');total+=x-v}if(total%8===0)count++}odd+=count;oddPer.push(count)}A(odd===98304,'Leech odd shell');
 return {ternary_golay:gh,hexacode:hh,binary_golay:bh,Niemeier_A2_12:{roots:72,determinant:1},Niemeier_D4_6:{roots:144,determinant:1},Coxeter_Todd:{min_norm:4,determinant:729,minimal_vectors:36+45*16},Leech:{min_norm:4,even_4_shell:4*276,even_2_shell:759*128,odd_shell:odd,odd_per_coordinate:oddPer,total:4*276+759*128+odd}}
}
function braid(){
 const mult=(a,b)=>[0,1,2,3].map(i=>(a[2*Math.floor(i/2)]*b[i%2]+a[2*Math.floor(i/2)+1]*b[2+i%2])%3),X=[1,1,0,1],Z=[1,0,2,1],I=[1,0,0,1];A(mult(mult(X,Z),X).join()===mult(mult(Z,X),Z).join(),'braid');
 const S=new Map([[I.join(),I]]),todo=[I];while(todo.length){const x=todo.pop();for(let g of [X,Z]){let y=mult(x,g);if(!S.has(y.join())){S.set(y.join(),y);todo.push(y)}}}A(S.size===24,'sympl');
 const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],conj=a=>[a[0],-a[1]],scale=(a,k)=>a.map(x=>x*k),phase=k=>[Math.cos(2*Math.PI*k/3),Math.sin(2*Math.PI*k/3)],mm=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((s,x,k)=>add(s,mul(x,b[k][j])),[0,0]))),adj=a=>a[0].map((_,i)=>a.map(row=>conj(row[i])));
 const F=V(1,3).map(([i])=>V(1,3).map(([j])=>scale(phase(i*j),1/Math.sqrt(3)))),P=F.map((row,i)=>row.map((_,j)=>i===j?phase(2*i*i):[0,0])),Q=mm(mm(F,P),adj(F)),L=mm(mm(P,Q),P),R=mm(mm(Q,P),Q);let overlap=[0,0];for(let i=0;i<3;i++)for(let j=0;j<3;j++)overlap=add(overlap,mul(conj(R[i][j]),L[i][j]));const z=scale(overlap,1/3);let err=0;for(let i=0;i<3;i++)for(let j=0;j<3;j++){let d=add(L[i][j],scale(mul(z,R[i][j]),-1));err+=d[0]**2+d[1]**2}A(err<1e-24,'quantum braid');return {symplectic_image_order:S.size,projective_Clifford_with_Paulis:216,braid_frobenius_residual:Math.sqrt(err),braid_relative_phase:z}
}
function simulator(C){
 let ideal=[];for(let g=1;g<=3;g++){let M=new Map();for(let L of C){function f(k,key){if(k===g){M.set(key,(M.get(key)||0)+1);return}for(let x of L)f(k+1,key+x.join(''))}f(0,'')}let h=hist([...M.values()]),den=8*9**g,unique=h[1]||0;A(unique*3**(2*g)===den*(3**g-1)*(3**g-3),'local USD');ideal.push({copies:g,outcome_multiplicity:h,USD:unique/den,local_minimum_error_success:M.size/den})}
 let erasure=[];for(let mask=1;mask<16;mask++){let inds=[0,1,2,3].filter(i=>mask>>i&1),M=new Map();for(let L of C){let cnt=new Map();for(let x of L){let k=inds.map(i=>x[i]).join('');cnt.set(k,(cnt.get(k)||0)+1)}for(let [k,v] of cnt){let a=M.get(k)||[];a.push(v);M.set(k,a)}}erasure.push({mask,sites:inds.length,success:[...M.values()].reduce((s,a)=>s+Math.max(...a),0)/72,unique_success:[...M.values()].filter(a=>a.length===1).reduce((s,a)=>s+a[0],0)/72})}
 let noisy=[];for(let e of [0,.001,.01,.05,.1]){let ok=0,wrong=0;const W=V(4,3),lab=W.map(x=>C.map((L,i)=>L.some(y=>y.join()===x.join())?i:-1).filter(i=>i>=0));for(let l=0;l<8;l++){let P=W.map(x=>C[l].reduce((s,y)=>s+x.reduce((t,a,i)=>t*(a===y[i]?1-e:e/2),1)/9,0));for(let i=0;i<81;i++)for(let j=0;j<81;j++){let a=lab[i].filter(k=>lab[j].includes(k));if(a.length===1){let v=P[i]*P[j]/8;if(a[0]===l)ok+=v;else wrong+=v}}}noisy.push({readout_symbol_error:e,correct:ok,incorrect:wrong,inconclusive:1-ok-wrong})}return {ideal,erasure,noisy}
}
function anomaly(){const F=[[3,2,1,1],[3,1,-4,-1],[3,1,2,-1],[1,2,-3,0],[1,1,6,0],[1,1,0,0]],a=[0,0,0,0,0,0];for(let [c,w,y,s] of F){a[0]+=w*s;a[1]+=(c===3?w*y:0);a[2]+=(w===2?c*y:0);a[3]+=c*w*y**3;a[4]+=c*w*y;a[5]+=w===2?c:0}A(a.slice(0,5).every(x=>x===0)&&a[5]%2===0,'SM anomaly');return {SM_16_anomaly:[...a.slice(0,5),a[5]%2],SU2_doublets:a[5],family_multiplicity_unrestricted:true,level1:[{embedding:'A2^4',c:8,roots:24,glue_roots:216},{embedding:'E6+A2',c:78/13+8/4,roots:78,glue_roots:162},{embedding:'D4+D4',c:2*28/7,roots:48,glue_roots:192}]}}
const C=planes(3,2,true).C;return {boundary:[planes(2,2).summary,planes(3,2).summary,planes(2,3).summary,planes(3,3).summary],higher_rank:[orbitDims(2,3),orbitDims(3,3),orbitDims(2,4),orbitDims(3,4),orbitDims(3,6)],pachner:pachner(C),lattices:codes(),braid:braid(),simulator:simulator(C),anomaly:anomaly()}
}
console.log(JSON.stringify(research(),null,2));
