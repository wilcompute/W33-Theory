function research(){
const mod=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},vec=n=>Array.from({length:3**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/3**(n-1-j))%3)),dot=(a,b)=>mod(a.reduce((s,x,i)=>s+x*b[i],0));
function geometry(){
 // characters of polynomial deformation complex; traces of Sym^3 computed directly in cyclotomic coefficient form.
 const mons=[];for(let a=0;a<=3;a++)for(let b=0;b<=3-a;b++)for(let c=0;c<=3-a-b;c++)mons.push([a,b,c,3-a-b-c]);
 const chi=(e,d)=>{let h=[0,0,0];for(let x of mons)h[dot(x,e)]++;return h},real=h=>h[0]-(h[1]+h[2])/2,abs2=h=>h.reduce((s,x)=>s+x*x,0)-h[0]*h[1]-h[1]*h[2]-h[2]*h[0];
 const types=[[0,0,0,0],[1,1,1,0],[2,2,2,0],[0,1,2,0]];
 const rows=types.map((e,i)=>{let h=[0,0,0];e.forEach(x=>h[x]++);let t=2*real(chi(e))-abs2(h)-1;return {eigen_exponents:e,polynomial_deformation_trace:t,h11_trace:[14,-4,-4,2][i]}});
 A(rows.map(x=>x.polynomial_deformation_trace).join()==='23,5,5,2','H21 traces');
 // irreducible character inner products: central trace and noncentral trace.
 let reps={};for(let k of ['h11_trace','polynomial_deformation_trace']){let [d,c1,c2,t]=rows.map(x=>x[k]);let triv=(d+c1+c2+24*t)/27,other=(d+c1+c2-3*t)/27,w=(d-(c1+c2)/2)/9;A(triv+8*other+6*w===d,'character');reps[k]={trivial:triv,each_nontrivial_linear:other,W:w,Wdual:w,restriction_to_free_C3:[(d+2*t)/3,(d-t)/3,(d-t)/3]}}
 // diagonal projective group on four coordinates. elements with multiplicities 2,1,1 are free.
 let V=vec(3),free=V.filter(v=>{let n=[0,0,0];v.concat(0).forEach(x=>n[x]++);return n.sort().join()==='1,1,2'}),lines=[],planes=[];
 for(let x of V.slice(1)){let l=[x,x.map(t=>mod(2*t))].map(x=>x.join()).sort();if(!lines.some(y=>y.join('|')===l.join('|')))lines.push(l)}
 for(let a of V.slice(1)){let p=V.filter(v=>dot(v,a)===0).map(v=>v.join()).sort();if(!planes.some(q=>q.join('|')===p.join('|')))planes.push(p)}
 let good=new Set(free.map(v=>v.join())),fp=planes.filter(P=>P.filter(x=>x!=='0,0,0').every(x=>good.has(x)));
 // all quotient spectra on H27: unweighted nearest generator Cayley. exact eig of 3x3 Harper: -2,1+-sqrt3.
 const high=[6,3-Math.sqrt(3),3+Math.sqrt(3)];
 const cover=[0,3,3,3,3,6,6,6,6,...high.flatMap(x=>Array(6).fill(x))];
 const axis=[0,3,3,...high.flatMap(x=>[x,x])],diagonal=[0,6,6,...high.flatMap(x=>[x,x])];
 const spectra={cover,axis,diagonal},mass=1;let det={};for(let [k,v] of Object.entries(spectra))det[k]={dimension:v.length,logdet:v.reduce((s,x)=>s+Math.log(x+mass*mass),0),heat_trace_t1:v.reduce((s,x)=>s+Math.exp(-x),0),heat_per_vertex:v.reduce((s,x)=>s+Math.exp(-x),0)/v.length};
 // all eight noncentral line lifts, axis vs diagonal, and normalized spectral determinant sign.
 return {deformation_traces:rows,representations:reps,diagonal_group:{order:27,free_elements:free.length,free_cyclic:lines.filter(l=>l.every(x=>good.has(x))).length,free_order9:fp.length,planes:planes.length},spectra,scalar_logdet:det,quotient_vs_cover_logdet:det.cover.logdet-det.axis.logdet,scope:'finite Cayley graph proxy, not CY Laplace spectrum'}
}
function magic(){
 let V=vec(3),ccz=0,inject=0;
 for(let x of V)for(let y of V)for(let z of V){let full=vec(2).slice(1).reduce((s,[u,v])=>s+mod(x[0]+x[1]*u+x[2]*v)*mod(y[0]+y[1]*u+y[2]*v)*mod(z[0]+z[1]*u+z[2]*v),0);A(mod(full+x[0]*y[0]*z[0])===0,'RM CCZ');ccz++}
 // data x, ancilla uniform y, measure y-x=t, remaining phase f(x+t); correct quadratic difference.
 for(let x of V)for(let t of V){let y=x.map((v,i)=>mod(v+t[i])),f=v=>mod(v[0]*v[1]*v[2]),q=mod(t[0]*x[1]*x[2]+t[1]*x[0]*x[2]+t[2]*x[0]*x[1]+t[0]*t[1]*x[2]+t[0]*t[2]*x[1]+t[1]*t[2]*x[0]+f(t));A(mod(f(y)-q-f(x))===0,'injection');inject++}
 const C=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>i===j?0:i===0||j===0?1:[1,4].includes((i-j+5)%5)?1:2));
 const G=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>+(i===j)).concat(C[i]).slice(1));
 let M=[];for(let i=0;i<6;i++)for(let j=0;j<6;j++)for(let k=0;k<6;k++)if(i||j||k)M.push(G[i].map((x,l)=>mod(x*G[j][l]*G[k][l])));
 let r=0;for(let j=0;j<11;j++){let i=M.findIndex((x,k)=>k>=r&&x[j]);if(i<0)continue;[M[i],M[r]]=[M[r],M[i]];let c=M[r][j];M[r]=M[r].map(x=>mod(x*c));for(let k=0;k<M.length;k++)if(k!==r){let f=M[k][j];M[k]=M[k].map((x,l)=>mod(x-f*M[r][l]))}r++}
 // heralded conversion CCZ resource to a single qutrit non-Clifford reflection: postselect b=c in + basis? use sum over b,c with phase x b c, x=0 9, nonzero3 => amplitude ratio 3:1:1, not unitary, magic.
 let amplitudes=[0,1,2].map(a=>{let h=[0,0,0];for(let b=0;b<3;b++)for(let c=0;c<3;c++)h[mod(a*b*c)]++;A(h[1]===h[2],'real');return h[0]-h[1]});
 A(amplitudes.join()==='9,3,3','postselection');
 return {RM_transversal_CCZ_tests:ccz,logical_phase:'CCZ^-1',injection_branch_tests:inject,branch_probability:1/27,Golay_weighted_CCZ_constraint_rank:r,Golay_weights_nullity:11-r,postselected_state:{unnormalized_ratio:[3,1,1],success:11/27},exact_ninth_root_obstruction:'relative amplitudes remain in Q(omega), zeta9 has degree 3 over it'}
}
function gravity(){
 const pairs=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)pairs.push([i,j]);
 const eps=a=>new Set(a).size!==4?0:(-1)**a.reduce((s,x,i)=>s+a.slice(i+1).filter(y=>y<x).length,0);
 const wedge=(a,b)=>pairs.reduce((s,p,i)=>s+pairs.reduce((t,q,j)=>t+a[i]*b[j]*eps(p.concat(q)),0),0);
 const rank=M=>{M=M.map(x=>x.slice());let r=0;for(let j=0;j<M[0].length;j++){let i=M.findIndex((x,k)=>k>=r&&Math.abs(x[j])>1e-9);if(i<0)continue;[M[i],M[r]]=[M[r],M[i]];let c=M[r][j];M[r]=M[r].map(x=>x/c);for(let k=r+1;k<M.length;k++){let f=M[k][j];M[k]=M[k].map((x,l)=>x-f*M[r][l])}r++}return r};
 // B identity tetrad: 6x6. simplicity derivative of B^I wedge B^J proportional to epsilon.
 const I=pairs.map((_,i)=>pairs.map((_,j)=>+(i===j))),B=[];
 for(let k=0;k<36;k++){let d=I.map(row=>row.map(()=>0));d[Math.floor(k/6)][k%6]=1;let v=[];for(let i=0;i<6;i++)for(let j=i;j<6;j++)v.push(wedge(d[i],I[j])+wedge(I[i],d[j]));B.push(v)}
 let base=[];for(let i=0;i<6;i++)for(let j=i;j<6;j++)base.push(wedge(I[i],I[j]));let k=base.findIndex(Boolean),constraints=base.map((x,i)=>B.map(v=>v[i]*base[k]-x*v[k]));let sr=rank(constraints);A(sr===20,'simplicity');
 // linear tetrad variation 16 columns
 let T=[];for(let k=0;k<16;k++){let a=Math.floor(k/4),b=k%4,d=pairs.flatMap(([i,j])=>pairs.map(([u,v])=>+(i===a&&u===b&&j===v)-+(i===a&&v===b&&j===u)+ +(j===a&&i===u&&v===b)-+(j===a&&i===v&&u===b)));A(constraints.every(row=>row.reduce((s,x,l)=>s+x*d[l],0)===0),'tetrad tangent');T.push(d)}A(rank(T)===16,'tetrad rank');
 const sym=[];for(let i=0;i<4;i++)for(let j=i;j<4;j++)sym.push([i,j]);let eta=[-1,1,1,1],rows=[];
 for(let p of [[1,0,0,0],[0,1,0,0],[1,0,0,1],[1,1,0,0]]){
 let k2=p.reduce((s,x,i)=>s+eta[i]*x*x,0),up=p.map((x,i)=>eta[i]*x),op=h=>{let tr=h.reduce((s,row,i)=>s+eta[i]*row[i],0),ph=h.map(row=>row.reduce((s,x,i)=>s+x*up[i],0)),pp=dotR(up,ph);return sym.map(([i,j])=>k2*h[i][j]-p[i]*ph[j]-p[j]*ph[i]+p[i]*p[j]*tr+(i===j?eta[i]*(pp-k2*tr):0))},dotR=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
 let M=sym.map(([i,j])=>op(Array.from({length:4},(_,u)=>Array.from({length:4},(_,v)=>+((u===i&&v===j)||(u===j&&v===i))))));
 let gauge=[];for(let k=0;k<4;k++){let h=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>p[i]*+(j===k)+p[j]*+(i===k)));A(op(h).every(x=>x===0),'gauge');gauge.push(sym.map(([i,j])=>h[i][j]))}
 let r=rank(M),gr=rank(gauge);rows.push({p,k2,operator_rank:r,gauge_rank:gr,physical_kernel:10-r-gr});A(10-r-gr===(k2===0?2:0),'spin2')}
 return {simplicity_rank:sr,tetrad_tangent_rank:16,linearized_Einstein:rows,scope:'continuum linearization with externally supplied tetrad/BF simplicity; no native finite Z3 graviton'}
}
function rg(){
 // eq33 near common c=1: dg/dt with t log UV/IR, N unit-charge Dirac species; e^2(t)=e0²/(1+N e0² t/(6pi²)).
 let rows=[];for(let N of [1,3,9,27,81])for(let decades of [10,20,40,100]){let t=decades*Math.LN10,e2=4*Math.PI/137,R=1+N*e2*t/(6*Math.PI**2),exp=(N+2)/N;rows.push({N,decades,ratio:R**(-exp),remaining_from_1_percent:.01*R**(-exp)})}
 return {linearized_difference_beta:'(N+2)e²/(6pi²) * delta',rows,scope:'published weak-coupling continuum QED, near c=1, identical fermion speeds, not microscopic QCA renormalization'}
}
return {geometry:geometry(),magic:magic(),gravity:gravity(),rg:rg()}
}
console.log(JSON.stringify(research(),null,2));
