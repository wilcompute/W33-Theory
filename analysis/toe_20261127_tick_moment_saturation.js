function saturation(){
const A=(v,s)=>{if(!v)throw Error(s)},m=x=>(x%3+3)%3,P=Array.from({length:81},(_,i)=>Array.from({length:4},(_,j)=>Math.floor(i/3**j)%3)).filter(v=>v.find(Boolean)===1),sp=(a,b)=>m(a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1]),lines=new Map();
for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)if(!sp(P[i],P[j])){let list=P.map((v,k)=>[v,k]).filter(([v])=>[0,1,2].some(a=>[0,1,2].some(b=>P[i].every((x,l)=>m(a*x+b*P[j][l])===v[l])))).map(x=>x[1]);A(list.length===4,'line');lines.set(list.join(),list)}
let ls=[...lines.values()];A(ls.length===40&&P.every((_,i)=>ls.filter(l=>l.includes(i)).length===4),'incidence');
let rows=[];for(let r=2;r<=24;r++){let e=3**(-r/2),u=Math.min(120,4+114*e,...(r>=5?[16/3]:r===4?[8]:r===2||r===3?[16]:[]));rows.push({r,lower:4,upper:u,asymptotic_bound:4+114*e})}
return {lines:ls.length,stabilizer_rays:360,rays_per_tick:12,commuting_other_tick_labels:36,noncommuting_tick_labels:81,rows,scope:"Analytical norm bound 4 <= ||M_r|| <= 4+114*3^-r/2. A direct sum of tick ranges has Gram diagonal I; commuting off-diagonals shared stabilizer ray, each ray repeated 3 times per row; noncommuting blocks norm 3^-r/2. Ray overlaps <=3^-r/2 give row quadratic bound. Monotonicity M_(r+1)<=M_r tensor I. M4 bound8 from four pairwise nonorthogonal isotropic replica directions, M5 max16/3. Incidence independently verified."}
}
console.log(JSON.stringify(saturation(),null,2));
