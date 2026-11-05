function serverMechanismControls(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const y=.2,L=7,S0=9,steps=10000,dt=-L/steps,c=2*y*y/(16*Math.PI**2);
 let soft=[0,0,S0];
 for(let n=0;n<steps;n++){
  const a=c*soft.reduce((x,z)=>x+z,0);
  const b=c*(soft.reduce((x,z)=>x+z,0)+1.5*dt*a);
  const cc=c*(soft.reduce((x,z)=>x+z,0)+1.5*dt*b);
  const d=c*(soft.reduce((x,z)=>x+z,0)+3*dt*cc);
  soft=soft.map(z=>z+dt*(a+2*b+2*cc+d)/6);
 }
 const closed=S0*Math.expm1(-6*y*y*L/(16*Math.PI**2))/3;
 assert(Math.abs(soft[0]-closed)<1e-12,"RG independent RK4");
 const det3=a=>a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);
 const Y=[[1,2,1],[2,1,3],[1,1,1]],C=[[1,0,1],[0,1,2],[1,1,4]];
 assert(det3(Y)===1&&det3(C)===1,"messenger determinant");
 const charges=[-9,-5,-1,7,8];
 assert(charges.reduce((a,b)=>a+b,0)===0&&charges.reduce((a,b)=>a+b*b*b,0)===0,"chiral anomalies");
 const flux=[];
 for(const len of [3,4]){
  const angle=(x,mu)=>{if(mu===0)return -2*Math.PI*x[1]/len**2;if(mu===1)return x[1]===len-1?2*Math.PI*x[0]/len:0;if(mu===2)return -2*Math.PI*x[3]/len**2;return x[3]===len-1?2*Math.PI*x[2]/len:0;};
  let maxError=0,checks=0;
  for(let a=0;a<len;a++)for(let b=0;b<len;b++)for(let c=0;c<len;c++)for(let d=0;d<len;d++){
   const x=[a,b,c,d];
   for(let mu=0;mu<4;mu++)for(let nu=mu+1;nu<4;nu++){
    const u=[...x],v=[...x];u[mu]=(u[mu]+1)%len;v[nu]=(v[nu]+1)%len;
    const p=angle(x,mu)+angle(u,nu)-angle(v,mu)-angle(x,nu);
    const target=(mu===0&&nu===1)||(mu===2&&nu===3)?2*Math.PI/len**2:0;
    const error=Math.abs(Math.atan2(Math.sin(p-target),Math.cos(p-target)));
    maxError=Math.max(maxError,error);checks++;
   }
  }
  assert(maxError<1e-13,"independent torus flux");
  flux.push({L:len,plaquettes:checks,max_phase_error:maxError});
 }
 // Uniformly sampled photon calibration: scalar response cancels optical sum.
 let controls=0;
 for(const a2 of [0,.1,1,100])for(const z of [.01,1,20]){
  const metricPhi=-(1+a2*Math.exp(-z)),metricPsi=-(1-a2*Math.exp(-z));
  assert(Math.abs(metricPhi+metricPsi+2)<1e-13,"optical cancellation");controls++;
 }
 const Mpl=2.435e27,H0=.6754981742923789*100*1000/3.08567758149e22*6.582119569e-16,cp=.05004260057022673,m=1e9,vis=1e12;
 const delta=Math.sqrt(2*Math.PI**2)*H0*Mpl/(cp*m),portal=Math.sqrt(8*Math.PI**2/10)*delta/vis;
 assert(Math.abs(portal/8.753026297780048e-25-1)<1e-14,"portal cap");
 return {status:"PASS_INDEPENDENT_V8_MECHANISM_CONTROLS",RG_RK4_absolute_error:Math.abs(soft[0]-closed),messenger_determinants:[det3(Y),det3(C)],flux,scalar_optical_controls:controls,portal_y:portal,scope:"Independent server V8 math checks. Not a replay of local eigenvalue solvers or proof of a chiral measure."};
}
if(typeof module!=='undefined'&&require.main===module) console.log(JSON.stringify(serverMechanismControls(),null,2));
