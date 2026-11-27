"use strict";
function run(){
const A=(b,m)=>{if(!b)throw Error(m)},arr=(n,f)=>Array.from({length:n},(_,i)=>f(i)),sum=a=>a.reduce((s,x)=>s+x,0),mod=(x,p=3)=>(x%p+p)%p,hist=a=>{let h={};for(let x of a)h[x]=(h[x]||0)+1;return h},dot=(a,b)=>sum(a.map((x,i)=>x*b[i])),pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
function determinant(){
 let z=sum(arr(100000,i=>1/(i+1)**4)),alt=sum(arr(100000,i=>(-1)**(i+1)/(i+1)**4));A(Math.abs(alt/z+7/8)<1e-12,"alternating");
 let rows=[];for(let nS of [0,1,4,8])for(let nD of [1,2,4]){let b=nS/2,per=b-2*nD,anti=b+7*nD/4;rows.push({real_scalars:nS,dirac_fermions:nD,periodic_logZ_coefficient:per,antiperiodic_logZ_coefficient:anti,logZ_sum_dominant:Math.max(per,anti)})}
 let hol=arr(9,j=>sum(arr(3000,i=>Math.cos(2*Math.PI*j*(i+1)/9)/(i+1)**4))/z);A(Math.abs(sum(hol)/9-1/9**4)<1e-11,"Z9 projection");
 return {zeta4:z,alternating_ratio:alt/z,short_axis_coefficient:2*z/Math.PI**2,rows,discrete_Z9_holonomy:hol,holonomy_mean:sum(hol)/9,scope:"4D Euclidean fixed-volume flat torus, positive masses, vectorlike Dirac absolute determinant, real boson. Leading short-cycle contribution; gauge ghost counting separate, no full chiral measure."}
}
function code(){
 const f=[[[0,0,0],1],[[1,0,0],1],[[0,1,0],2],[[0,0,1],2]],g=[[[1,0,0],1],[[0,1,0],1],[[0,0,1],1],[[1,1,0],1],[[1,0,1],1],[[0,1,1],1]];
 let terms=new Map();for(let [a,c] of f)for(let [b,d] of f){let k=a.map((x,i)=>x+b[i]).join(",");terms.set(k,mod((terms.get(k)||0)+c*d))}let digit=[...terms].filter(x=>x[1]).map(([k,c])=>[k.split(",").map(Number),c]);A(digit.length===10,"digit");
 let rows=[];for(let n=1;n<=5;n++){let L=3**n,sy=new Map(),support=new Map(),max=0,steps=0,enc=(x,y,z)=>mod(x,L)+L*(mod(y,L)+L*mod(z,L)),add=(s,k,c)=>{let v=mod((s.get(k)||0)+c);if(v)s.set(k,v);else s.delete(k)},apply=(x,y,z,c)=>{let k=enc(x,y,z);A(!support.has(k),"unique monomial");add(support,k,c);for(let [[a,b,d],e] of f)add(sy,enc(x+a,y+b,z+d),c*e);max=Math.max(max,sy.size);steps++};
 function rec(k,x,y,z,c){if(!k){apply(x,y,z,c);return}let h=3**(k-1);for(let [[a,b,d],e] of digit)rec(k-1,x+h*a,y+h*b,z+h*d,mod(c*e))}
 rec(n,0,0,0,1);A(sy.size===0&&steps===10**n&&max<=4+36*n,"fractal");let proj=new Map();for(let [v,c] of support)add(proj,v%L,c);A(proj.size===L&&[...proj.values()].every(c=>c===1),"nontrivial quotient");
 let ranks=null;if(L<=9){let N=L**3,base=new Array(N),rank=0;for(let k=0;k<N;k++)for(let polynomial of [f,g]){let x=k%L,y=Math.floor(k/L)%L,z=Math.floor(k/L**2),r=new Uint8Array(N);for(let [[a,b,d],e] of polynomial)r[enc(x+a,y+b,z+d)]=e;for(let j=0;j<N;j++){let v=r[j];if(!v)continue;if(!base[j]){if(v===2)for(let i=j;i<N;i++)r[i]=mod(2*r[i]);base[j]=r;rank++;break}for(let i=j;i<N;i++)r[i]=mod(r[i]-v*base[j][i])}}ranks={rank_per_check:rank,k:2*N-2*rank};A(ranks.k===4*L-2,"rank theorem")}
 rows.push({L,physical_qutrits:2*L**3,logical_qutrits:4*L-2,weight:steps,maximum_defects:max,final_defects:sy.size,projection_weight:proj.size,rank_check:ranks})}
 const inv=(a,b)=>{let norm=mod(a*a+b*b),z=norm===1?1:2;return [mod(a*z),mod(-b*z)]};let roots=[];for(let s of [1,2]){let r=[[1,s],[0,s],[1,0]].map(([a,b])=>inv(a,b).map(x=>mod(-x)));A(new Set(r.map(x=>x.join())).size===3,"distinct roots");roots.push(r)}
 return {rows,monomial_digit_count:digit.length,F9_affine_roots:roots,scope:"Translation invariant qutrit CSS polynomial model; charge no-binomial test on infinite lattice, not general finite-width logical no-string theorem or thermal stability."}
}
function polarity(){
 let pts=[...new Set(arr(81,i=>{let v=arr(4,j=>Math.floor(i/3**j)%3),c=v.find(Boolean);return c?v.map(x=>mod(c*x)).join(""):""}).filter(Boolean))].map(x=>x.split("").map(Number));
 let forms=arr(729,i=>arr(6,j=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),pf=v=>mod(v[0]*v[5]-v[1]*v[4]+v[2]*v[3]),pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],pl=(a,b)=>pairs.map(([i,j])=>mod(a[i]*b[j]-a[j]*b[i])),canon=v=>v.map(x=>mod(x*v.find(Boolean))).join(""),lines=new Map();
 for(let i=0;i<40;i++)for(let j=i+1;j<40;j++){let p=pl(pts[i],pts[j]);lines.set(canon(p),p)}
 let nd=forms.filter(v=>pf(v)),sets=nd.map(v=>new Set([...lines].filter(([_,p])=>dot(v,p)%3===0).map(([k])=>k)));A(forms.length===364&&nd.length===234&&lines.size===130&&sets.every(s=>s.size===40),"polar forms");
 let overlap={},byClass={};for(let i=0;i<nd.length;i++)for(let j=i+1;j<nd.length;j++){let n=[...sets[i]].filter(x=>sets[j].has(x)).length;overlap[n]=(overlap[n]||0)+1;let k=(pf(nd[i])===pf(nd[j])?"same":"opposite")+":"+n;byClass[k]=(byClass[k]||0)+1}
 A(Object.values(overlap).reduce((a,b)=>a+b,0)===234*233/2,"overlap count");A(pts.every(u=>nd.every(v=>pts.filter(w=>dot(v,pl(u,w))%3===0).length===13)),"polar plane");
 const N=117,rows=[];for(let h of [0,.1,.5,1,2,4]){let J=1,a=-J-2*h/N,b=-2*h*(N-1)/N,c=-2*h*Math.sqrt(N-1)/N,E=(a+b-Math.sqrt((a-b)**2+4*c*c))/2,p=(1-(a-b)/Math.sqrt((a-b)**2+4*c*c))/2;rows.push({h,ground_energy_symmetric_block:E,aligned_probability:h===0?1:p})}
 return {projective_forms:forms.length,degenerate:forms.length-nd.length,nondegenerate:nd.length,pfaffian_classes:hist(nd.map(pf)),pair_intersection_histogram:overlap,byClass,selected_isotropic_lines:40,ferromagnet_two_site_symmetric_block:rows,scope:"Chosen order-parameter register with invariant ferromagnet; no anyon condensation of nonbosonic selector, no dynamical preference between Pfaffian sectors."}
}
function gravity(){
 const rank=M=>{M=M.map(r=>r.slice());let n=0;for(let j=0;j<M[0].length&&n<M.length;j++){let k=M.findIndex((r,i)=>i>=n&&Math.abs(r[j])>1e-10);if(k<0)continue;[M[n],M[k]]=[M[k],M[n]];let p=M[n][j];M[n]=M[n].map(x=>x/p);for(let i=n+1;i<M.length;i++){let v=M[i][j];M[i]=M[i].map((x,l)=>x-v*M[n][l])}n++}return n};
 let dirs=[[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,-1,0],[1,0,1],[1,0,-1],[0,1,1],[0,1,-1]],dyad=([x,y,z])=>[x*x,y*y,z*z,2*x*y,2*x*z,2*y*z],D=dirs.map(dyad),tt=dirs.map(([x,y,z])=>[x*x-y*y,2*x*y]);A(rank(D.slice(0,3))===3&&rank(D)===6&&rank(tt.slice(0,3))===1&&rank(tt)===2,"tensor ranks");
 let N=24,m=1,chi=[0,.5,1,2,4].map(nu=>{let diag=0,cross=0,mix=0;for(let i=0;i<N;i++)for(let j=0;j<N;j++)for(let k=0;k<N;k++){let p=[i,j,k].map(v=>2*Math.PI*v/N),h=p.map(x=>2*Math.sin(x/2)),w=Math.sqrt(m*m+dot(h,h)),a=h[0]**2-h[1]**2,b=2*Math.sin(p[0])*Math.sin(p[1]),weight=1/(2*w*(4*w*w+nu*nu));diag+=weight*a*a;cross+=weight*b*b;mix+=weight*a*b}return {nu,plus:diag/N**3,cross:cross/N**3,mixed:mix/N**3}});
 A(chi.every(x=>Math.abs(x.mixed)<1e-12)&&chi.every((x,i)=>!i||x.plus<chi[i-1].plus&&x.cross<chi[i-1].cross),"susceptibility");
 return {axial_tensor_rank:3,augmented_tensor_rank:6,axial_TT_rank:1,augmented_TT_rank:2,scalar_shear_susceptibility:chi,scope:"Homogeneous q=0 shear control in cubic oscillator lattice, distinct finite-spacing vertices; no general diffeo Ward identity or induced graviton. Bare stiffness tuning required."}
}
function rotor(){
 let even=arr(32,i=>i).filter(i=>pop(i)%2===0),gamma=(i,s)=>{let j=i>>1,b=(s>>j)&1;return [s^(1<<j),mod(2*pop(s&((1<<j)-1))+(i%2?1+2*b:0),4)]},C=s=>{let phase=0;for(let j=4;j>=0;j--){let [t,k]=gamma(2*j,s);s=t;phase=mod(phase+k,4)}return [s,phase]},B=(i,s)=>{let [t,k]=gamma(i,s),[v,l]=C(t);return [v,mod(k+l,4)]};
 for(let a=0;a<10;a++)for(let b=0;b<10;b++){let re=0,im=0;for(let s of even){let [u,v]=B(a,s),[w,x]=B(b,s);if(u===w){let p=mod(x-v,4);re+=[1,0,-1,0][p];im+=[0,1,0,-1][p]}}A(re===16*+(a===b)&&im===0,"pair gram")}
 let rows=[];for(let D of [.5,1,2,4])for(let g of [.1,.5,1,2]){let E=(D-Math.hypot(D,8*g))/2,Ev=(D-Math.hypot(D,8*g/Math.sqrt(10)))/2;A(E<Ev&&Ev<0,"unique scalar");rows.push({rotor_gap:D,g,ground:E,next:Ev,gap:Ev-E,vector_multiplicity:10,pair_probability:(1-D/Math.hypot(D,8*g))/2})}
 let r=rows.find(r=>r.rotor_gap===1&&r.g===1);return {pair_gram_diagonal:16,pair_gram_checks:100,rotor_dimension:11,fermion_dimension_truncated:529,full_truncated_dimension:5819,rows,two_site_gap_bound:[0,.25,.5].map(J=>({J,lower_bound:r.gap-2*J})),scope:"Exactly diagonalized symmetry-preserving projected on-site rotor (l<=1) and 0,1,2 fermions, no Weyl hopping or full rotor. Two-site perturbation bound, no thermodynamic gap."}
}
return {status:"PASS",determinant:determinant(),ternary_code:code(),polarity:polarity(),gravity:gravity(),rotor:rotor()}
}
console.log(JSON.stringify(run(),null,2));
