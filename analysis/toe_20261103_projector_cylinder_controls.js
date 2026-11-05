function cylinderControls(){
 const mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],conj=a=>[a[0],-a[1]];
 const pow=(z,n)=>{let r=[1,0];while(n){if(n%2)r=mul(r,z);z=mul(z,z);n=Math.floor(n/2);}return r;};
 const phase=t=>[Math.cos(t),Math.sin(t)],dist=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
 const theta0=.4,theta1=1.2,expected=phase(Math.PI*(Math.cos(theta1)-Math.cos(theta0))),rows=[];
 function hol(theta,N){
  const c=Math.cos(theta/2)**2,s=Math.sin(theta/2)**2,d=2*Math.PI/N;
  const overlap=[c+s*Math.cos(d),-s*Math.sin(d)],norm=Math.hypot(...overlap);
  return pow(overlap.map(x=>x/norm),N);
 }
 for(const N of [128,512,2048,8192]){
  const ratio=mul(hol(theta1,N),conj(hol(theta0,N)));
  rows.push({steps:N,ratio_complex:ratio,cylinder_phase_error:dist(ratio,expected)});
 }
 if(!(rows[3].cylinder_phase_error<2e-7&&rows[2].cylinder_phase_error<rows[1].cylinder_phase_error))throw Error("Cylinder convergence failed");
 const flatLoop=phase(2*Math.PI*.5);
 return {status:"PASS_SERVER_PROJECTOR_CYLINDER_AND_GLOBAL_LOOP_CONTROL",theta0,theta1,
 analytic_curvature:"Omega_theta_phi = -sin(theta)/2 for P=|v><v|,v=(cos(theta/2),e^(i phi)sin(theta/2))",
 expected_ratio_complex:expected,rows,
 flat_connection_control:{one_form:"(1/2)dphi on S1",curvature:0,loop_Wilson_phase_complex:flatLoop},
 scope:"Prior Berry/Kato rank-one cylinder identity and flat global-holonomy counterexample. A numerical geometry control, NOT the four-dimensional fermion measure, its locality, SU5 proof, or independent verification of all claims of arXiv2610.09093.",
 source:"https://arxiv.org/html/2610.09093v1#S5"};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(cylinderControls(),null,2));
