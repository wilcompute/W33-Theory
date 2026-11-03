/* Independent controls first executed on the V8 server during local DC validation. */
function crosscheck(){
  const found=new Set();
  for(let a=-200;a<=200;a++)for(let b=a;b<=200;b++){const c=9-a-b;if(c<b||c>200)continue;if(a*a*a+b*b*b+c*c*c===81)found.add([a,b,c].join(","));}
  const expected=["-18,10,17","-15,12,12","3,3,3"];
  if(found.size!==3||expected.some(x=>!found.has(x)))throw Error("charge enumeration");
  const L=[[1,-2,-1,2],[2,1,2,1]],K=[1,1,-1,-1];
  const U=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>4*L.reduce((t,r)=>t+r[i]*r[j],0)+(i===j?5:0)));
  for(let i=0;i<4;i++)for(let j=0;j<4;j++){
    const v=U.reduce((s,r,k)=>s+U[i][k]*K[k]*U[k][j],0);
    if(v!==((i===j)?225*K[i]:0))throw Error("mirror characteristic");
  }
  const minors=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)minors.push(L[0][i]*L[1][j]-L[0][j]*L[1][i]);
  function gcd(a,b){return b?gcd(b,a%b):Math.abs(a);}
  if(minors.reduce(gcd)!==1)throw Error("primitive lattice");
  const cap=Math.pow(2*Math.PI*Math.PI,.25)*Math.sqrt((100*.6754981742923789*1000/3.085677581491367e22*6.582119569e-16)*2.435e27/.05004260057022673);
  function mul(A,B){return A.map((row,i)=>B[0].map((_,j)=>row.reduce((out,z,k)=>[out[0]+z[0]*B[k][j][0]-z[1]*B[k][j][1],out[1]+z[0]*B[k][j][1]+z[1]*B[k][j][0]],[0,0])));}
  let checks=0;
  const signs=[[1,1],[1,-1],[-1,1],[-1,-1]];
  for(const gamma of [0,.5,1])for(const t of [.1,.7]){
    const rho=signs.map((v,i)=>signs.map((w,j)=>{const h=(v[0]!==w[0]?1:0)+(v[1]!==w[1]?1:0),a=-(v[0]*v[1]-w[0]*w[1])*t,r=Math.exp(-2*gamma*t*h)/4;return[r*Math.cos(a),r*Math.sin(a)];}));
    const M=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>rho[2*Math.floor(i/2)+j%2][2*Math.floor(j/2)+i%2]));
    const p=Math.exp(-2*gamma*t),ev=[(1+p*p+2*p*Math.cos(2*t))/4,(1+p*p-2*p*Math.cos(2*t))/4,(1-p*p+2*p*Math.sin(2*t))/4,(1-p*p-2*p*Math.sin(2*t))/4];
    let power=M;
    for(let n=1;n<=4;n++){const tr=power.reduce((s,r,i)=>s+r[i][0],0),im=power.reduce((s,r,i)=>s+r[i][1],0),e=ev.reduce((s,v)=>s+v**n,0);if(Math.abs(tr-e)>1e-12||Math.abs(im)>1e-12)throw Error("PPT moments");checks++;power=mul(power,M);}
  }
  return{status:"PASS_INDEPENDENT_SERVER_PHYSICS_CONTROLS",sterile_charge_box:200,sterile_integer_solutions:[...found].sort(),bounded_enumeration_is_not_the_global_proof:true,mirror_integer_velocity_numerator:U,mirror_primitive_minors:minors,mirror_characteristic_identity:"U K U=225 K, V=U/15",independent_Dovekie_negative_branch_CW_mass_cap_eV:cap,PPT_trace_moment_checks:checks,scope:"Independent V8 server arithmetic, with no Python producer imports. It corroborates the declared benchmarks; no complete TOE or empirical discovery."};
}
if(typeof module!=='undefined'){module.exports={crosscheck};if(require.main===module)process.stdout.write(JSON.stringify(crosscheck(),null,2)+'\n');}
