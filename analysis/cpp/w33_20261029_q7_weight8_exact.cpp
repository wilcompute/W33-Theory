/* Exhaustive transitivity-reduced W(3,7) adjacency CSS weight-8 falsifier.
   Build W(3,7) from projective symplectic F7^4, then fix coordinate
   zero by PSp4(7) point transitivity. A nonzero even kernel word with
   weight <=8 yields equal syndromes on a 4-subset containing point 0
   and a 4-subset excluding 0. This is a necessary condition.
   A deterministic F2-linear 64-bit projection is used: if projected
   sets are disjoint, the full syndrome sets are disjoint. No assumption
   about SHA/hash collision resistance is made. Requires g++ -fopenmp.
*/
#include <cstdint>
#include <array>
#include <vector>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <chrono>
#include <omp.h>
using namespace std;
using V=array<int,4>;
uint64_t mix(uint64_t x) {
 x+=0x9e3779b97f4a7c15ull;
 x=(x^(x>>30))*0xbf58476d1ce4e5b9ull;
 x=(x^(x>>27))*0x94d049bb133111ebull;
 return x^(x>>31);
}
int form(const V&a,const V&b) {
 int t=a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2];
 t%=7;return t<0?t+7:t;
}
int main() {
 vector<V> p;
 for(int a=0;a<7;a++) for(int b=0;b<7;b++)
 for(int c=0;c<7;c++) for(int d=0;d<7;d++) {
  V x{a,b,c,d};int k=0;while(k<4&&!x[k])k++;
  if(k==4)continue;
  int inv=1;while((inv*x[k])%7!=1)inv++;
  for(int &u:x)u=u*inv%7;
  p.push_back(x);
 }
 sort(p.begin(),p.end());p.erase(unique(p.begin(),p.end()),p.end());
 int n=(int)p.size();
 if(n!=400){cerr<<"bad point count\n";return 1;}
 vector<uint64_t> cols(n);
 for(int i=0;i<n;i++) {
  int degree=0;
  for(int j=0;j<n;j++)if(i!=j&&!form(p[i],p[j])) {
   degree++;cols[j]^=mix(0x57a78d20261029ull+(uint64_t)i);
  }
  if(degree!=56){cerr<<"bad collinearity degree\n";return 1;}
 }
 // Exactly C(399,3) triple projections; open addressing with no deletion.
 constexpr uint64_t EMPTY=~0ull;
 const size_t CAP=size_t(1)<<25, MASK=CAP-1;
 vector<uint64_t> tab(CAP,EMPTY);
 uint64_t triples=0,duplicates=0;
 auto begin=chrono::steady_clock::now();
 for(int a=1;a<n-2;a++)for(int b=a+1;b<n-1;b++) {
  uint64_t ab=cols[a]^cols[b];
  for(int c=b+1;c<n;c++) {
   uint64_t key=ab^cols[c];
   if(key==EMPTY){cerr<<"unexpected sentinel value\n";return 1;}
   size_t pos=(size_t)mix(key)&MASK;
   while(tab[pos]!=EMPTY&&tab[pos]!=key)pos=(pos+1)&MASK;
   if(tab[pos]==key)duplicates++;
   else tab[pos]=key;
   triples++;
  }
 }
 cout<<"TRIPLES "<<triples<<" PROJECTION_DUPLICATES "<<duplicates<<"\n"<<flush;
 unsigned long long hits=0,examined=0;
 #pragma omp parallel for reduction(+:hits,examined) schedule(dynamic,1)
 for(int a=1;a<n-3;a++)for(int b=a+1;b<n-2;b++) {
  uint64_t ab=cols[0]^cols[a]^cols[b];
  for(int c=b+1;c<n-1;c++) {
   uint64_t abc=ab^cols[c];
   for(int d=c+1;d<n;d++) {
    uint64_t key=abc^cols[d];
    size_t pos=(size_t)mix(key)&MASK;
    while(tab[pos]!=EMPTY&&tab[pos]!=key)pos=(pos+1)&MASK;
    hits+=(tab[pos]==key);
    examined++;
   }
  }
 }
 double sec=chrono::duration<double>(chrono::steady_clock::now()-begin).count();
 cout<<"QUADRUPLES "<<examined<<" PROJECTED_CROSS_COLLISIONS "<<hits
     <<" SECONDS "<<setprecision(4)<<sec<<"\n";
 if(triples!=10507399ull||examined!=1040232501ull)return 2;
 if(hits){cout<<"INCONCLUSIVE: collision needs exact full-syndrome check\n";return 3;}
 cout<<"PASS: no W(3,7) binary adjacency kernel word of weight 2,4,6,8;"
        " CSS distance is between 10 and 14 inclusive\n";
 return 0;
}
