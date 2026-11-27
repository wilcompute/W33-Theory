function rankCertificate(){
const A=(x,s)=>{if(!x)throw Error(s)},K=60,S=10n**18n,bin=Array.from({length:2*K+1},()=>Array(2*K+1).fill(0n));
for(let n=0;n<=2*K;n++){bin[n][0]=bin[n][n]=1n;for(let k=1;k<n;k++)bin[n][k]=bin[n-1][k-1]+bin[n-1][k]}
let returns=Array(K+1).fill(0n);returns[0]=1n;let rows=[];
for(let d=1;d<=54;d++){returns=Array.from({length:K+1},(_,k)=>{let z=0n;for(let j=0;j<=k;j++)z+=bin[2*k][2*j]*bin[2*j][j]*returns[k-j];return z});
let low=0n,high=0n;for(let k=1;k<=K;k++){let j=BigInt(k),den=BigInt(2*d)**(2n*j)*2n*j;low+=S*returns[k]*25n**j/(den*36n**j);high+=S*returns[k]/(den*4n**j)}
// Tail D_low <= (25/36)^(K+1) / (2(K+1)(1-25/36)); D_high analogous.
let ceil=(a,b)=>(a+b-1n)/b,tl=ceil(S*25n**BigInt(K+1)*36n,36n**BigInt(K+1)*BigInt(2*(K+1))*11n),th=ceil(S*4n,4n**BigInt(K+1)*BigInt(2*(K+1))*3n);
let lo=10n*high-3n*(low+BigInt(K)+tl),hi=10n*(high+BigInt(K)+th)-3n*low;rows.push({d,lo:lo.toString(),hi:hi.toString(),relative_bulk_logweight:[Number(lo)/Number(S),Number(hi)/Number(S)]})}
let best=rows[3];A(rows.every(x=>x.d===4||BigInt(x.hi)<BigInt(best.lo)),"finite separation");A(725n*S<55000n*BigInt(best.lo),"tail bound"); // 0.725/55
return {rows,selected_rank:4,exact_scale:S.toString(),tail_bound_at_55:0.725/55,nearest_competitor:rows.filter(x=>x.d!==4).reduce((a,b)=>BigInt(a.hi)>BigInt(b.hi)?a:b),scope:"Exact integer return counts + rational truncation intervals for ranks1..54; log weight relative to infinite-rank limit. For d>=55, 10 D_high -3 D_low <= 10 E[X²](-log(1-1/4)/2) = (2.5/d)log(4/3) < .725/d (alternating log or rational bound). Thus global maximum d4 for supplied masses .2,1 and signed multiplicities3,-10. No physical derivation of parameters, flat geometry and total hop normalization supplied."}
}
console.log(JSON.stringify(rankCertificate(),null,2));
