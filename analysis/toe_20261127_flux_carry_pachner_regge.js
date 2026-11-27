function lifts(){
 const m=(x,n)=>(x%n+n)%n,A=(x,s)=>{if(!x)throw Error(s)},sg=x=>x===2?-1:x,rows=[],V=Array.from({length:243},(_,i)=>Array.from({length:5},(_,j)=>Math.floor(i/3**j)%3)).map(v=>v.concat(m(-v.reduce((s,x)=>s+x,0),3)));
 let checks=0;for(let v of V){let digits=[0,0,0],sum=0;for(let f of v){let a=sg(f)+1;sum+=a;for(let i=0;i<3;i++){let b=digits[i]+a;digits[i]=b%3;a=Math.floor(b/3)}A(digits[0]+3*digits[1]+9*digits[2]===sum,'carry accumulation');checks++}let j=v.reduce((s,x)=>s+sg(x),0)/3;A(digits[0]===0&&digits[1]+3*digits[2]-2===j,'quotient');}
 for(let k=1;k<=10;k++){let classes={};for(let j=-2;j<=2;j++){let key=m(3*j,3*k);(classes[key]??=[]).push(j)}rows.push({clock_order:3*k,classes,distinguishes_signed:Object.values(classes).every(v=>v.length===1),distinguishes_squared:Object.values(classes).every(v=>v.every(j=>j*j===v[0]*v[0]))})}
 // Fit even Fourier action on the computed quotient clock j modulo 9.
 let c1=j=>1-Math.cos(2*Math.PI*j/9),c2=j=>1-Math.cos(4*Math.PI*j/9),D=c1(1)*c2(2)-c1(2)*c2(1),a=(c2(2)-4*c2(1))/D,b=(4*c1(1)-c1(2))/D,max=0;
 for(let v of V){let j=v.reduce((s,x)=>s+sg(x),0)/3;max=Math.max(max,Math.abs(a*c1(j)+b*c2(j)-j*j))}A(max<1e-12,'Fourier');
 return {carry_checks:checks,rows,quotient_clock_fourier:{a,b,max_error:max},scope:"Reversible modular addition of supplied principal-lift increments into three ternary digits; the quotient j can then be read on a Z9 clock. Direct total-flux Z9 aliases charges; Z27 first ternary power sufficient. Fourier coefficients fitted, not dynamically derived."}
}
function pachner(){
const m=x=>(x%3+3)%3,A=(x,s)=>{if(!x)throw Error(s)},E=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==3||j!==4)E.push([i,j]);let ix=new Map(E.map((x,i)=>[x.join(),i])),census={},witness={};let f=(v,i,j,k)=>m(v[ix.get([i,j].join())]+v[ix.get([j,k].join())]-v[ix.get([i,k].join())]);
for(let n=0;n<3**9;n++){let v=E.map((_,i)=>Math.floor(n/3**i)%3),F=f(v,0,1,2),d=[0,1,2].map(i=>m(v[ix.get([i,3].join())]-v[ix.get([i,4].join())])),pattern=[...new Set(d)].length,key=F+','+pattern;census[key]=(census[key]||0)+1;witness[key]??={edge_values:v,d}}
let rows=[];for(let t of [.1,.5,1,2]){let w=x=>1+Math.exp(-t)*(x===0?2:-1);let L=w(0),R=[0,1,2].map(g=>w(g)**3).reduce((s,x)=>s+x,0)/3;let norm=L/R;
let x=Object.entries(witness).map(([key,v])=>{let [F,p]=key.split(',').map(Number),r=[0,1,2].reduce((s,g)=>s+v.d.reduce((p,d)=>p*w(m(g+d)),1),0)/3;return {F,distinct_offsets:p,old:w(F),new_after_flat_normalization:norm*r,ratio:norm*r/w(F)}});rows.push({t,values:x});A(x.some(v=>v.F===0&&Math.abs(v.ratio-1)>1e-6),'nonclosure')}
let geom=[];for(let h of [.4,.8,1.2]){let L2=h*h+1/3,flat=2*h,theta=d=>2*Math.asin(1/(2*Math.sqrt(L2-d*d/4))),def=d=>2*Math.PI-3*theta(d),vol=d=>d*(L2-d*d/4)*Math.sin(theta(d))/2,old=Math.sqrt(3)*h/6;A(Math.abs(def(flat))<1e-12&&Math.abs(vol(flat)-old)<1e-12,'flat geometry');let hess=(def(flat+1e-5)-def(flat-1e-5))/2e-5;geom.push({h,flat_internal_edge:flat,volume:old,deficit:def(flat),Regge_length_action_second_derivative:hess})}
return {boundary_assignments:3**9,classes:census,witness,rows,geom,scope:"3D bipyramid 2-3 move, same boundary gauge weights canceled. Internal face heat kernels fail closure after any constant normalization at fixed coupling; boundary-dependent effective weights needed. Euclidean Regge flat stationary length with boundary term, not gauge-gravity unification."}
}
console.log(JSON.stringify({lifts:lifts(),pachner:pachner()},null,2));
