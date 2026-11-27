function tests(){
const m=x=>(x%3+3)%3,A=(v,s)=>{if(!v)throw Error(s)},rank=(M)=>{M=M.map(r=>Uint8Array.from(r));let r=0;for(let j=0;j<M[0].length;j++){let i=M.findIndex((x,k)=>k>=r&&x[j]);if(i<0)continue;[M[i],M[r]]=[M[r],M[i]];if(M[r][j]===2)for(let k=j;k<M[0].length;k++)M[r][k]=m(2*M[r][k]);for(let k=r+1;k<M.length;k++){let f=M[k][j];if(f)for(let l=j;l<M[0].length;l++)M[k][l]=m(M[k][l]-f*M[r][l])}r++}return r};
let tensor=[];
for(let L of [2,3,4,5]){
let N=L**3,pairs=[[0,0],[1,1],[2,2],[0,1],[0,2],[1,2]],shift=(v,d)=>{let p=L**d,x=Math.floor(v/p)%L;return v+(x===L-1?1-L:1)*p},d=(v,i)=>[[shift(v,i),1],[v,-1]],dd=(v,i,j)=>d(v,i).flatMap(([u,a])=>d(u,j).map(([w,b])=>[w,a*b]));
let X=Array.from({length:3*N},()=>new Uint8Array(6*N)),Z=Array.from({length:N},()=>new Uint8Array(6*N));
for(let v=0;v<N;v++)for(let c=0;c<6;c++){let [i,j]=pairs[c];for(let [u,a] of d(v,i))X[3*u+j][6*v+c]=m(X[3*u+j][6*v+c]+a);for(let [u,a] of d(v,j))X[3*u+i][6*v+c]=m(X[3*u+i][6*v+c]+a);
let terms=i===j?[0,1,2].filter(k=>k!==i).flatMap(k=>dd(v,k,k)):dd(v,i,j).map(([u,a])=>[u,-2*a]);for(let [u,a] of terms)Z[v][6*u+c]=m(Z[v][6*u+c]+a)}
let nonzero=0;for(let z of Z)for(let x of X){let s=0;for(let j=0;j<x.length;j++)if(z[j])s+=z[j]*x[j];A(m(s)===0,'commute');nonzero++}
let rx=rank(X),rz=rank(Z);tensor.push({L,N,qudits:6*N,rankX:rx,rankZ:rz,logical:6*N-rx-rz,commutator_checks:nonzero,semisimple:L%3!==0});if(L%3)A(rx===3*(N-1)&&rz===N-1,'ranks');
}
let disp=[.2,.1,.05,.025].map(k=>{let d=2*Math.sin(k/2);return {k,curvature_squared_frequency:d*d,curvature_bilinear_frequency:d,ratio_z2:d*d/k,ratio_z1:d/k}});
let high=[6,3-Math.sqrt(3),3+Math.sqrt(3)].flatMap(x=>[x,x]),S=[[0,3,3],[3,6,6],[3,6,6]].map(x=>x.concat(high)),D=mass=>{let l=S.map(x=>x.reduce((s,y)=>s+Math.log(y+mass**2),0)/9);return l[0]-l.reduce((s,x)=>s+x,0)/3};
let soft=[];for(let mb of [.5,1,2])for(let mf of [.5,1,2]){let v=D(mb)-D(mf);A(Math.sign(v)===Math.sign(mb-mf),'split sign');soft.push({boson_mass:mb,fermion_mass:mf,net_difference:v})}
let supertrace=0,torsion=0;let bin=[1,6,15,20,15,6,1];for(let q=0;q<=6;q++){supertrace+=(-1)**q*bin[q];torsion+=(-1)**q*q*bin[q]}
A(supertrace===0&&torsion===0,'de Rham pairing');
return {tensor,dispersion:disp,scalar_superpartner_proxy:soft,flat_six_dimensional_mode_supertrace:supertrace,flat_six_dimensional_torsion_weight:torsion}
}
console.log(JSON.stringify(tests(),null,2));
