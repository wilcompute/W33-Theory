function gravityAndVacuum(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},rank=M=>{M=M.map(r=>Uint8Array.from(r));let r=0;for(let j=0;j<M[0].length;j++){let i=M.findIndex((x,k)=>k>=r&&x[j]);if(i<0)continue;[M[r],M[i]]=[M[i],M[r]];if(M[r][j]===2)for(let k=j;k<M[0].length;k++)M[r][k]=m(2*M[r][k]);for(let k=r+1;k<M.length;k++){let f=M[k][j];if(f)for(let l=j;l<M[0].length;l++)M[k][l]=m(M[k][l]-f*M[r][l])}r++}return r},eps=(a,b,c)=>new Set([a,b,c]).size<3?0:((a-b)*(b-c)*(c-a)>0?1:-1),tensor=[];
for(let L of [2,3,4]){
let N=L**3,P=[[0,0],[1,1],[2,2],[0,1],[0,2],[1,2]],shift=(v,d)=>{let p=L**d;return v+(Math.floor(v/p)%L===L-1?1-L:1)*p},d=(v,i)=>[[shift(v,i),1],[v,-1]],dd=(v,i,j)=>d(v,i).flatMap(([u,a])=>d(u,j).map(([w,b])=>[w,a*b]));
let X=Array.from({length:3*N},()=>new Uint8Array(6*N)),Z=Array.from({length:6*N},()=>new Uint8Array(6*N)),R=Array.from({length:N},()=>new Uint8Array(6*N));
for(let v=0;v<N;v++)for(let c=0;c<6;c++){let [i,j]=P[c];for(let [u,a] of d(v,i))X[3*u+j][6*v+c]=m(X[3*u+j][6*v+c]+a);for(let [u,a] of d(v,j))X[3*u+i][6*v+c]=m(X[3*u+i][6*v+c]+a);
for(let t=0;t<6;t++){let [k,l]=P[t];for(let a=0;a<3;a++)for(let b=0;b<3;b++){let w=eps(i,a,k)*eps(j,b,l)+(k!==l?eps(i,a,l)*eps(j,b,k):0);if(w)for(let [u,z] of dd(v,a,b))Z[6*v+c][6*u+t]=m(Z[6*v+c][6*u+t]+w*z)}}
}
for(let v=0;v<N;v++)for(let j=0;j<6*N;j++)R[v][j]=m(Z[6*v][j]+Z[6*v+1][j]+Z[6*v+2][j]);
let checks=0;for(let z of Z)for(let x of X){let s=0;for(let j=0;j<x.length;j++)if(z[j])s+=z[j]*x[j];A(m(s)===0,'double curl commute');checks++}
let rx=rank(X),rz=rank(Z),rr=rank(R);if(L%3)A(rx===3*(N-1)&&rz===3*(N-1),'semisimple');let hist={};for(let z of Z){let w=z.filter(Boolean).length;hist[w]=(hist[w]||0)+1}tensor.push({L,sites:N,physical_qutrits:6*N,rankX:rx,rankScalar:rr,rankDoubleCurl:rz,original_logicals:6*N-rx-rr,closed_logicals:6*N-rx-rz,checks,curvature_weight_histogram:hist,independent_projector_parent_gap:1});
}
let h0=[[1,0,0,1],[0,6,9,0],[0,9,6,0],[1,0,0,1]],h1=[[0,0,0,0],[0,4,7,0],[0,7,4,0],[0,0,0,0]],hX=h0.map((r,i)=>r.map((v,j)=>v+2*h1[i][j])),chi=H=>H.map(r=>r.reduce((s,x,q)=>s+(-1)**q*x,0)),bcov=H=>H.reduce((s,r,p)=>s+r.reduce((z,x,q)=>z+(-1)**(p+q)*p*q*x,0),0);
A(chi(h0).join()===chi(h1).join(),'Euler chars');
let radial=[];for(let R of [.25,.5,1,2,4,8]){let B=.5,F=2,u=1;let v=-(Math.exp(-B*B*R*R*u)-Math.exp(-F*F*R*R*u))/R**16;radial.push({R,einstein_frame_integrand:v})}A(radial.every((x,i)=>!i||x.einstein_frame_integrand>radial[i-1].einstein_frame_integrand),'monotonic');
return {tensor,holomorphic:{cover:hX,trivial:h0,nontrivial:h1,chi_Omega_cover:chi(hX),chi_Omega_quotient:chi(h0),chi_Omega_twisted:chi(h1),BCOV_zero_mode_weights:{cover:bcov(hX),trivial:bcov(h0),nontrivial:bcov(h1)},torsion_relation:'log T_p(E_chi)=log T_(3-p)(E_conjugate_chi); BCOV weighted sum reduces to log T_1 - 3 log T_0 for real/trivial twists'},radial,scope:'commuting-projector tensor Hamiltonian exact gapped control; uniform-scale matched scalar-like soft mass potential monotonic, not full string stabilization'}
}
console.log(JSON.stringify(gravityAndVacuum(),null,2));
