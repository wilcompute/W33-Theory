function qec(){
 const m=x=>(x%3+3)%3, word=(a,b)=>[b,m(a+b),m(a-b)], dot=(x,y)=>m(x.reduce((s,v,i)=>s+v*y[i],0)), s=[1,1,2];
 const errs=[];for(let i=0;i<3;i++)for(let x=0;x<3;x++)for(let z=0;z<3;z++)if(x||z){let u=[0,0,0],v=[0,0,0];u[i]=x;v[i]=z;let synd=[dot(s,u),dot(s,v)];if(synd.every(a=>a===0))throw Error('undetected');errs.push({i,x,z,synd})}
 const census={};for(let e of errs)census[e.synd.join()]=(census[e.synd.join()]||0)+1;
 if(Object.values(census).some(x=>x!==3)||Object.keys(census).length!==8)throw Error('syndrome');
 // diagonal transversal ninth-root phases: local phase f_i(0)=0; f_i(1), f_i(2) mod9.
 const mod9=x=>(x%9+9)%9;let preserved=0,logical={};
 for(let i=0;i<9**6;i++){let k=i,f=Array.from({length:3},()=>{let a=k%9;k=Math.floor(k/9);let b=k%9;k=Math.floor(k/9);return [0,a,b]});let E=Array.from({length:3},(_,a)=>Array.from({length:3},(_,b)=>mod9(word(a,b).reduce((t,v,j)=>t+f[j][v],0))));if(E.some(e=>e.some(x=>x!==e[0])))continue;preserved++;let phase=E.map(e=>mod9(e[0]-E[0][0]));logical[phase.join()]=(logical[phase.join()]||0)+1}
 if(Object.keys(logical).some(k=>k.split(',').some(x=>Number(x)%3)))throw Error('non-Clifford');
 // all 9 logical phase pairs modulo3 are quadratic => Clifford.
 return {code:'[[3,1,2]]_3',single_site_nonidentity_errors:errs.length,syndrome_multiplicities:census,all_ninth_root_transversal_candidates:9**6,preserving_assignments:preserved,logical_phases_mod9:logical,independent_erasure_success:'1-3e^2+2e^3',scope:'known-location one erasure; unknown-location errors detected but not corrected; diagonal product ninth-root phases only'};
}
console.log(JSON.stringify(qec(),null,2));
