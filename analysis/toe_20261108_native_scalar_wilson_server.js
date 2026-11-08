// Independent actual-server check: convergent binomial matrix series, no eigensolver.
function nativeWilsonServer(fixture) {
  const N=27, mass=3, L=2, n=2, alpha=10+mass*mass, rho=10/alpha, terms=64;
  function multiply(P,Q) {
    const R=new Float64Array(2*N*N);
    for(let i=0;i<N;i++)for(let k=0;k<N;k++){
      const a=2*(i*N+k), pr=P[a],pi=P[a+1];
      if(pr===0&&pi===0)continue;
      for(let j=0;j<N;j++){const b=2*(k*N+j),c=2*(i*N+j);
        R[c]+=pr*Q[b]-pi*Q[b+1];R[c+1]+=pr*Q[b+1]+pi*Q[b];
      }
    } return R;
  }
  function block(k) {
    const Q=new Float64Array(2*N*N);
    fixture.a.forEach((i,e)=>{
      const j=fixture.b[e],t=fixture.V[e].reduce((s,v,d)=>s+v*k[d],0);
      Q[2*(i*N+j)]+=Math.cos(t)/alpha;Q[2*(i*N+j)+1]+=Math.sin(t)/alpha;
      Q[2*(j*N+i)]+=Math.cos(t)/alpha;Q[2*(j*N+i)+1]-=Math.sin(t)/alpha;
    });
    let P=new Float64Array(2*N*N);for(let i=0;i<N;i++)P[2*(i*N+i)]=1;
    let sum=0,co=.5;
    for(let l=1;l<=terms;l++){
      P=multiply(P,Q);let tr=0;for(let i=0;i<N;i++)tr+=P[2*(i*N+i)];
      sum+=co*tr;co*= (l-.5)/(l+1);
    }
    return {energy:Math.sqrt(alpha)*(N-sum),tail:Math.sqrt(alpha)*N*co*rho**(terms+1)/(1-rho)};
  }
  function energy(theta){
    let sum=0,tail=0;
    for(let a=0;a<n;a++)for(let b=0;b<n;b++)for(let c=0;c<n;c++)for(let d=0;d<L;d++){
      const r=block([2*Math.PI*a/n,2*Math.PI*b/n,2*Math.PI*c/n,(2*Math.PI*d+theta)/L]);
      sum+=r.energy;tail+=r.tail;
    }
    return {theta,energy:sum/n**3,rigorous_series_tail_bound:tail/n**3};
  }
  const h=.04,rows=[-2*h,-h,0,h,2*h,Math.PI].map(energy);
  const curvature=(-rows[4].energy+16*rows[3].energy-30*rows[2].energy+16*rows[1].energy-rows[0].energy)/(12*h*h);
  return {runtime:"Actual functions.exec V8",method:"Full27x27 complex binomial matrix powers; independent of Python eigensolver/Frechet curvature.",
    grid:n,L,mass,terms,alpha,rho,rows,five_point_curvature:curvature,
    delta_V_pi:rows[5].energy-rows[2].energy,
    truncation_scope:"Scalar binomial coefficient positive and decreasing; ||A/alpha||<=10/alpha by graph degree10. Geometric bound controls analytic series truncation only, not floating point or finite-difference/infinite-volume error."};
}
