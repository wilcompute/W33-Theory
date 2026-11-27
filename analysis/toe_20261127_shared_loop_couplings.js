function sharedCoupling(){
 const C=t=>2/3*Math.log((1+t+t*t)/((1-t)**2)),A=(v,s)=>{if(!v)throw Error(s)};
 let lo=0,hi=1;for(let i=0;i<80;i++){let t=(lo+hi)/2;if(13.5*C(t)<1)lo=t;else hi=t}let t=(lo+hi)/2,r=t**(1/12),mu=13.5*C(t);
 let rows=Array.from({length:10},(_,i)=>({wilson_copies:i+1,beta:(i+1)*C(t),mu,within_published_interval:(i+1)*C(t)>.265&&(i+1)*C(t)<.512}));
 A(Math.abs(mu-1)<1e-12&&rows.filter(x=>x.within_published_interval).map(x=>x.wilson_copies).join()==="4,5,6",'target');
 // Compare unequal length convention. Gauge-only single face loops length4; paired loops length8; twisted loops length12.
 let f=C(r**4),p=C(r**8),q=C(r**12);
 let unpadded={single_face_coeff:-f,same_sign_pair_coeff:-2*p,difference_pair_coeff:2*q,required_same_sign_pair:-2*f,required_difference_pair:2*f};
 // A length-12 directed loop transfer C: det(I-r C)=1-r^12 holonomy, and Gaussian M^dagger M is positive.
 return {common_padded_length:12,hop_amplitude:r,loop_amplitude:t,mu,rows,unpadded,scope:"Padding supplied via neutral inverse pairs; Wilson multiplicity 4-6 chosen by comparison with published numerical interval at mu=1, not derived or predicted. Auxiliary Gaussian action positive definite for r<1. No new phase simulation."}
}
console.log(JSON.stringify(sharedCoupling(),null,2));
