// Independent ordinary-Monte-Carlo integration on the actual server V8 runtime.
// A gamma(3,1) rejection sampler replaces the PC inverse-CDF/Sobol method.
function scalarSelfServer(input, count = 131072) {
  let state = 246813579;
  const uniform = () => { state ^= state << 13; state ^= state >>> 17; state ^= state << 5; return ((state >>> 0) + .5) / 4294967296; };
  const dot = (a,b) => a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3];
  const plus = (a,b) => a.map((x,i)=>x+b[i]);
  const direction = () => { const z=2*uniform()-1,t=2*Math.PI*uniform(),s=Math.sqrt(1-z*z);return [s*Math.cos(t),s*Math.sin(t),z]; };
  const momentum = () => {
    let q; do {q=-Math.log(uniform()*uniform()*uniform());} while(uniform()>Math.exp(q-Math.hypot(q,input.r)));
    const d=direction(),k=q/input.r;return [Math.hypot(1,k),...d.map(x=>k*x)];
  };
  const boost = (a,b) => {
    const b2=b.reduce((s,x)=>s+x*x,0),g=1/Math.sqrt(1-b2),bp=b.reduce((s,x,i)=>s+x*a[i+1],0);
    const c=(b2>1e-20?(g-1)/b2:.5)*bp+g*a[0];
    return [g*(a[0]+bp),...b.map((x,i)=>a[i+1]+c*x)];
  };
  const ratio = (x,table) => {
    const q=input.q;if(x>q[q.length-1])return 0;
    let lo=0,hi=q.length-1;while(hi-lo>1){const mid=(lo+hi)>>1;if(q[mid]>x)hi=mid;else lo=mid;}
    const t=Math.max(0,(x-q[lo])/(q[hi]-q[lo]));return Math.exp(table[lo]*(1-t)+table[hi]*t);
  };
  const sums=input.points.map(()=>[0,0,0,0]);
  for(let sample=0;sample<count;sample++) {
    const incoming=[momentum(),momentum(),momentum()],P=incoming.reduce(plus,[0,0,0,0]),s=dot(P,P);
    const E=Math.sqrt(s)/2,k=Math.sqrt(s/4-1),d=direction(),b=P.slice(1).map(x=>x/P[0]);
    const finals=[boost([E,...d.map(x=>k*x)],b),boost([E,...d.map(x=>-k*x)],b)];
    const legs=[...incoming,...finals.map(x=>x.map(v=>-v))],pairs=[];
    for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){const a=plus(legs[i],legs[j]);pairs.push({i,j,value:1/(dot(a,a)-1)});}
    let single=0,double=0;
    for(let i=0;i<pairs.length;i++) {
      single+=pairs[i].value;
      for(let j=i+1;j<pairs.length;j++){const a=pairs[i],b=pairs[j];if(a.i!==b.i&&a.i!==b.j&&a.j!==b.i&&a.j!==b.j)double+=a.value*b.value;}
    }
    const momenta=legs.map(x=>Math.hypot(...x.slice(1))*input.r);
    input.points.forEach((point,index)=>{
      const g3=Math.sqrt(18*point.lambdaS),g4=6*point.lambdaS,amp=g3*g4*single+g3**3*double;
      const weight=Math.sqrt(1-4/s)*amp*amp/incoming.reduce((a,x)=>a*x[0],1);
      const ratios=momenta.map(q=>ratio(q,point.log_ratio));
      const fw=weight*ratios[0]*ratios[1]*ratios[2],bw=weight*ratios[3]*ratios[4];
      sums[index][0]+=fw;sums[index][1]+=bw;sums[index][2]+=fw*fw;sums[index][3]+=bw*bw;
    });
  }
  return {runtime:'Actual server V8; independent gamma-rejection ordinary MC',count,r:input.r,
    scope:'Independent 3<->2 integration at r=1 on interpolated frozen parent histories. No self-consistent transport or remote-PC execution claimed.',
    rows:input.points.map((point,index)=>{
      const v=sums[index],factor=input.n_eq**3/(768*Math.PI)*point.units;
      return {M_keV:point.M_keV,gamma32_over_nS_H:factor*v[0]/count,gamma23_over_nS_H:factor*v[1]/count,
        estimated_standard_error:[2,3].map((j,i)=>factor*Math.sqrt(Math.max(0,v[j]/count-(v[i]/count)**2)/count))};
    })};
}
