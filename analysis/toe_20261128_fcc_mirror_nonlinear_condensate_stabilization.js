"use strict";
function run(){
const A=(x,m)=>{if(!x)throw Error(m)},arr=(n,f)=>Array.from({length:n},(_,i)=>f(i)),sum=a=>a.reduce((s,x)=>s+x,0),mod=(x,p=3)=>(x%p+p)%p,dot=(a,b)=>sum(a.map((x,i)=>x*b[i])),mat=(n,m,f)=>arr(n,i=>arr(m,j=>f(i,j))),tr=a=>a[0].map((_,i)=>a.map(r=>r[i])),mul=(a,b)=>mat(a.length,b[0].length,(i,j)=>dot(a[i],b.map(r=>r[j])));
function eig(a){a=a.map(r=>r.slice());let n=a.length;for(let sweep=0;sweep<80;sweep++){let mx=0;for(let p=0;p<n;p++)for(let q=p+1;q<n;q++){let b=a[p][q];mx=Math.max(mx,Math.abs(b));if(Math.abs(b)<1e-13)continue;let z=(a[q][q]-a[p][p])/(2*b),t=(z>=0?1:-1)/(Math.abs(z)+Math.hypot(1,z)),c=1/Math.hypot(1,t),s=t*c;a[p][p]-=t*b;a[q][q]+=t*b;a[p][q]=a[q][p]=0;for(let k=0;k<n;k++)if(k!==p&&k!==q){let u=a[k][p],v=a[k][q];a[k][p]=a[p][k]=c*u-s*v;a[k][q]=a[q][k]=s*u+c*v}}if(mx<1e-11)return a.map((r,i)=>r[i]).sort((x,y)=>x-y)}throw Error("eig")}
function fcc(){
 const roots=[];for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)for(let a of [-1,1])for(let b of [-1,1]){let v=[0,0,0];v[i]=a;v[j]=b;roots.push(v)}
 const axes=arr(6,i=>arr(3,j=>j===Math.floor(i/2)?2*(i%2?1:-1):0)),mean=(v,f)=>sum(v.map(f))/v.length,dirs=[[1,0,0],[1,1,0].map(x=>x/Math.sqrt(2)),[1,1,1].map(x=>x/Math.sqrt(3))],moments=dirs.map(n=>({n,raw2:mean(roots,r=>dot(r,n)**2),raw4:mean(roots,r=>dot(r,n)**4),improved2:(16*mean(roots,r=>dot(r,n)**2)+mean(axes,r=>dot(r,n)**2))/17,improved4:(16*mean(roots,r=>dot(r,n)**4)+mean(axes,r=>dot(r,n)**4))/17,improved6:(16*mean(roots,r=>dot(r,n)**6)+mean(axes,r=>dot(r,n)**6))/17}));A(moments.every(r=>Math.abs(r.improved4-16/17)<1e-12&&Math.abs(r.improved2-12/17)<1e-12),"moments");
 const z=(a=0,b=0)=>[a,b],add=(a,b)=>z(a[0]+b[0],a[1]+b[1]),neg=a=>z(-a[0],-a[1]),cm=(a,b)=>z(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]),co=a=>z(a[0],-a[1]),sc=(a,s)=>z(a[0]*s,a[1]*s),abs=a=>Math.hypot(...a),cs=a=>a.reduce(add,z()),ct=a=>tr(a).map(r=>r.map(co)),mm=(a,b)=>mat(a.length,b[0].length,(i,j)=>cs(a[i].map((x,k)=>cm(x,b[k][j])))),err=(a,b)=>Math.max(...a.flat().map((v,i)=>abs(add(v,neg(b.flat()[i]))))),zero=(n,m)=>mat(n,m,()=>z()),norm=a=>sum(a.map(x=>abs(x)**2));
 let s=Math.SQRT1_2,E=[[[1,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,1]],[[0,s,0],[s,0,0],[0,0,0]],[[0,0,s],[0,0,0],[s,0,0]],[[0,0,0],[0,0,s],[0,s,0]]],dual=[[.5,.5,-.5],[.5,-.5,.5],[-.5,.5,.5]],checks=0,res=0,samples=[];
 for(let L of [3,4,7,8,12])for(let a=0;a<L;a++)for(let b=0;b<L;b++)for(let c=0;c<L;c++){if(!(a||b||c))continue;let q=[a,b,c].map(x=>z(Math.cos(2*Math.PI*x/L)-1,Math.sin(2*Math.PI*x/L))),d=arr(3,i=>cs(q.map((x,j)=>sc(x,dual[j][i])))),d2=cs(d.map(x=>cm(x,x))),n=norm(d);A(n>1e-12,"doubler");
 let G=mat(6,3,(i,j)=>sc(cs(d.map((x,l)=>sc(x,E[i][l][j]))),2)),C=[E.map(e=>add(sc(d2,e[0][0]+e[1][1]+e[2][2]),neg(cs(arr(3,i=>cs(arr(3,j=>sc(cm(d[i],d[j]),e[i][j]))))))))],cn=norm(C[0]),X=[[z(),neg(d[2]),d[1]],[d[2],z(),neg(d[0])],[neg(d[1]),d[0],z()]],K=mat(6,6,(i,j)=>{let h=mm(mm(X,E[j].map(r=>r.map(x=>z(x)))),tr(X));return cs(h.flat().map((v,k)=>sc(v,E[i].flat()[k])))});
 let V=mm(ct(K),K),T=mat(6,6,(i,j)=>add(z(i===j?cn:0),neg(cm(co(C[0][i]),C[0][j])))),diff=Math.max(err(mm(C,G),zero(1,3)),err(mm(K,G),zero(6,3)),err(mm(C,T),zero(1,6)),err(mm(V,V),V.map(r=>r.map(v=>sc(v,n*n)))),Math.abs(cs(V.map((r,i)=>r[i]))[0]-3*n*n),Math.abs(cn-(abs(d2)**2+n*n)));res=Math.max(res,diff);A(diff<1e-8,"complex constraint");
 checks++;if(b===0&&c===0&&a===1)samples.push({L,omega_local:n*Math.sqrt(cn),d_norm:Math.sqrt(n),ratio_z4:n*Math.sqrt(cn)/(n*n)});
 }
 return {moments,checks,res,samples,scope:"Local forward-difference tensor constraints on FCC primitive translations, two degenerate modes but z=4; relativistic spectral normalization nonlocal."}
}
function mirror(){
 let rows=[];for(let t of [.005,.01,.02,.05,.1,.2]){let energies=[];for(let k=0;k<=32;k++){let n=35;if(k>0&&k<32){n=34;let H=mat(n,n,(i,j)=>i===j?1:0);let a=k+1;H[0][0]=H[a][a]=.5;H[0][a]=H[a][0]=-.5;for(let j=0;j<k;j++)H[j][j+1]=H[j+1][j]=t*Math.sqrt((j+1)*(k-j));for(let j=0;j<32-k;j++)H[a+j][a+j+1]=H[a+j+1][a+j]=t*Math.sqrt((j+1)*(32-k-j));energies.push(eig(H)[0]);}else{let H=mat(n,n,(i,j)=>i===j?1:0);for(let i of [0,1,33,34])H[i][i]=.5;H[0][1]=H[1][0]=H[33][34]=H[34][33]=-.5;for(let j=0;j<32;j++)H[j+1][j+2]=H[j+2][j+1]=t*Math.sqrt((j+1)*(32-j));energies.push(eig(H)[0]);}}
 let sym=Math.max(...energies.map((e,k)=>Math.abs(e-energies[32-k])));A(sym<1e-10,"particle-hole");rows.push({t,energies,bandwidth:Math.max(...energies)-Math.min(...energies),second_order:-16*t*t,center_minus_k1:energies[16]-energies[1],scaled_difference:(energies[16]-energies[1])/t**4,symmetry_residual:sym})}
 return {rows,mirror_modes:32,target_modes:32,atomic_gap:1,scope:"Invariant Krylov sectors of projector-cat mirror surrogate plus local target hopping; not full rotor numerical spectrum. Full rotor second-order spectral argument separate."}
}
function nonlinear(){
 let L=7,D=mat(L,L,(i,j)=>+(j===mod(i+1,L))-+(j===mod(i-1,L))),U=D.map((r,i)=>r.map(x=>x*+(i===0))),V=D.map((r,i)=>r.map(x=>x*+(i===1))),UV=mul(U,V),VU=mul(V,U),K=UV.map((r,i)=>r.map((x,j)=>x-VU[i][j]));A(K[0][2]===1&&D[0][2]===0,"closure");
 return {L,central_difference_scaled_by_two:true,commutator:K,witness:[0,2,1],rows:[8,16,32,64,128,256].map(L=>{let k=2*Math.PI/L;return {L,defect:Math.abs(Math.sin(2*k)-2*Math.sin(k)),relative:Math.abs(Math.sin(2*k)-2*Math.sin(k))/(2*Math.sin(k))}}),scope:"Obstruction to naive local vector-field bracket closure, not exclusion of nonlinear lattice gravity."}
}
function condensation(){
 const vals=arr(729,i=>arr(6,j=>Math.floor(i/3**j)%3)),Q=v=>mod(v[0]*v[5]-v[1]*v[4]+v[2]*v[3]),B=(a,b)=>mod(a[0]*b[5]+a[5]*b[0]-a[1]*b[4]-a[4]*b[1]+a[2]*b[3]+a[3]*b[2]),N=vals.filter(v=>v.find(Boolean)===1&&Q(v)===0),rows=[];
 for(let r=0;r<=6;r++){let hist={},total=0,example=null,min=131;function piv(p,start){if(p.length===r){let R=mat(r,6,(i,j)=>+(p[i]===j)),free=[];for(let i=0;i<r;i++)for(let j=p[i]+1;j<6;j++)if(!p.includes(j))free.push([i,j]);function fill(k){if(k<free.length){let [i,j]=free[k];for(let t=0;t<3;t++){R[i][j]=t;fill(k+1)}return}let count=0;for(let b of N)if(R.every(a=>B(a,b)===0))count++;hist[count]=(hist[count]||0)+1;total++;if(count<min){min=count;example=R.map(r=>r.slice())}}fill(0);return}for(let j=start;j<=6-(r-p.length);j++)piv(p.concat(j),j+1)}piv([],0);rows.push({r,total,hist,min,example,unconfined_anyon_count:3**(12-2*r)})}
 A(rows.map(r=>r.total).join()==="1,364,11011,33880,11011,364,1","Gaussian");A(rows[1].hist[40]===234&&rows[1].hist[49]===130,"W33");
 const lower=Math.max(...rows.slice(2).map(r=>(40-r.min)/(r.r-1))),mu=60;A(lower<mu&&mu<90,"selection");
 function rank3(M){let R=[],p=[];for(let v of M){v=v.map(x=>mod(x));for(let i=0;i<R.length;i++){let c=v[p[i]];v=v.map((x,j)=>mod(x-c*R[i][j]))}let k=v.findIndex(Boolean);if(k>=0){let c=v[k];R.push(v.map(x=>mod(x*c)));p.push(k)}}return R.length}
 const L=2,V=L*L,E=2*V,idx=(x,y)=>mod(x,L)+L*mod(y,L),e=(x,y,d)=>2*idx(x,y)+d,D=mat(V,E,()=>0),P=mat(V,E,()=>0);
 for(let x=0;x<L;x++)for(let y=0;y<L;y++){let v=idx(x,y);for(let d=0;d<2;d++){let j=e(x,y,d),w=idx(x+(d===0),y+(d===1));D[v][j]--;D[w][j]++}for(let [j,c] of [[e(x,y,0),1],[e(x+1,y,1),1],[e(x,y+1,0),-1],[e(x,y,1),-1]])P[v][j]+=c}
 A(mul(P,tr(D)).every(r=>r.every(x=>x===0))&&rank3(P)===3&&rank3(D)===3,"torus CSS");
 return {rows,lower_cost_in_units_delta:lower,upper_cost_in_units_delta:90,chosen_cost:mu,rank_energies:rows.map(r=>mu*r.r-(130-r.min)),torus:{vertices:V,edges:E,rank_vertex:rank3(D),rank_face:rank3(P),remaining_logical_qutrits:5*(E-rank3(D)-rank3(P))},scope:"All subspaces enumerated; rank cost plus effective probes and conditional quantum-double projectors, classical selectors."}
}
function holonomy(){
 let rows=[];for(let s of [1,.7,.4,.25]){let F=0,F2=0,tw=arr(8,()=>0),M=16;for(let x=-2*M;x<=2*M;x++)for(let y=-2*M;y<=2*M;y++)for(let z=-2*M;z<=2*M;z++){if(!(x||y||z))continue;let r2=(s*x)**2+(y*y+z*z)/s,w=1/(r2*r2);for(let j=0;j<8;j++)tw[j]+=(-1)**mod((j&1)*x+((j>>1)&1)*y+((j>>2)&1)*z,2)*w;if(Math.max(Math.abs(x),Math.abs(y),Math.abs(z))<=M)F+=w;if(x%2===0&&y%2===0&&z%2===0)F2+=w}
 A(Math.abs(sum(tw)-F/2)<1e-8*Math.max(1,F)&&Math.abs(F2-F/16)<1e-10*Math.max(1,F),"twist projection");rows.push({s,F,twist_sum:sum(tw),ratio:sum(tw)/F,cutoff:M})}
 return {rows,weyl_charged:729,maxwell_coefficient:1,neutral_dirac_twist_sets:731,total_neutral_dirac:5848,uniform_log_weight_coefficient:-1,scope:"Massless free vacuum shape weight per unit time, fixed covolume spatial torus, all eight background Z2 characters; supplied neutral matter sector."}
}
return {status:"PASS",fcc:fcc(),mirror:mirror(),nonlinear:nonlinear(),condensation:condensation(),holonomy:holonomy()}
}
console.log(JSON.stringify(run(),null,2));
