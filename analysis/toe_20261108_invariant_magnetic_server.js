// Independent server control of native6x6 area compensation, not full135edge replay.
function invariantMagneticServer() {
  const M=[[10,5,-6,0],[5,10,0,-6],[-6,0,12,-6],[0,-6,-6,12]];
  const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], c=29857/5775,alpha=1/16;
  const target=pairs.map(([i,j])=>pairs.map(([k,l])=>(M[i][k]*M[j][l]-M[i][l]*M[j][k])/27));
  const complement=target.map((r,i)=>r.map((x,j)=>x-(i===0&&j===0?alpha*c:0)));
  function bilinear(x,A,y){return x.reduce((s,a,i)=>s+a*y.reduce((t,b,j)=>t+A[i][j]*b,0),0);}
  function chol(A){let L=A.map(r=>r.map(()=>0));for(let i=0;i<A.length;i++)for(let j=0;j<=i;j++){let s=A[i][j];for(let k=0;k<j;k++)s-=L[i][k]*L[j][k];L[i][j]=i===j?Math.sqrt(s):s/L[j][j];}return L;}
  const L0=chol(target),forward=Array(6).fill(0),inverseColumn=Array(6).fill(0);
  for(let i=0;i<6;i++){let s=i===0?1:0;for(let j=0;j<i;j++)s-=L0[i][j]*forward[j];forward[i]=s/L0[i][i];}
  for(let i=5;i>=0;i--){let s=forward[i];for(let j=i+1;j<6;j++)s-=L0[j][i]*inverseColumn[j];inverseColumn[i]=s/L0[i][i];}
  const relativeEigenvalue=c*inverseColumn[0];
  const L=chol(complement);let cholError=0;
  for(let i=0;i<6;i++)for(let j=0;j<6;j++){let v=0;for(let k=0;k<6;k++)v+=L[i][k]*L[j][k];cholError=Math.max(cholError,Math.abs(v-complement[i][j]));}
  const cases=[];
  for(const n of [[1,0,0,0],[0,0,1,0],[1,2,-1,1],[-2,3,1,4]]) {
    const raw=[.7,-.2,.4,1.3],nn=bilinear(n,M,n),proj=bilinear(n,M,raw)/nn;
    const x=raw.map((a,i)=>a-proj*n[i]);
    const y=pairs.map(([i,j])=>n[i]*x[j]-n[j]*x[i]);
    const short=alpha*c*y[0]**2,added=bilinear(y,complement,y),predicted=nn*bilinear(x,M,x)/27;
    cases.push({n,x,short,added,total:short+added,predicted,transverse:bilinear(n,M,x)});
  }
  return {runtime:'Actual functions.exec V8',M,pairs,short_coefficient:c,alpha,target,complement,
    Cholesky_diagonal:L.map((r,i)=>r[i]),Cholesky_max_error:cholError,cases,
    relative_rank_one_eigenvalue:relativeEigenvalue,PSD_short_weight_threshold:1/relativeEigenvalue,
    scope:'Independent native6x6 area positivity and transverse common-speed algebra. Not fullnative Bloch, exact rational normal-equation or135edge covariance replay.'};
}
