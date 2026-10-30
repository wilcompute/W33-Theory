// Exhaustive q7 FOUR-line union kernel theorem, reduced by symplectic
// transitivity of W(3,7) on isotropic lines.
// Compile: g++ -O3 -std=c++20 -o q7four analysis/cpp/w33_20261029_q7_four_line_fixed.cpp
// Run: ./q7four
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;using B=array<U,7>;
struct V{array<int,4> a;bool operator<(V const&o)const{return a<o.a;}};
int main(){const int q=7;set<V> sp;
 for(int a=0;a<q;a++)for(int b=0;b<q;b++)for(int c=0;c<q;c++)for(int d=0;d<q;d++){
 array<int,4>x{a,b,c,d};int k=0;while(k<4&&!x[k])k++;if(k==4)continue;int z=1;while(z*x[k]%q!=1)z++;V v;for(int j=0;j<4;j++)v.a[j]=z*x[j]%q;sp.insert(v);
 }
 vector<V>P(sp.begin(),sp.end());assert(P.size()==400);
 auto form=[&](int i,int j){auto &a=P[i].a,&b=P[j].a;int v=a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2];return(v%q+q)%q;};
 vector<B>A(400);for(auto& a:A)a.fill(0);
 for(int i=0;i<400;i++)for(int j=0;j<400;j++)if(i!=j&&!form(i,j))A[i][j/64]|=U(1)<<(j%64);
 vector<B>L;for(int i=0;i<400;i++)for(int j=i+1;j<400;j++)if(A[i][j/64]>>(j%64)&1){B v{};for(int k=0;k<7;k++)v[k]=A[i][k]&A[j][k];v[i/64]|=U(1)<<(i%64);v[j/64]|=U(1)<<(j%64);L.push_back(v);}
 sort(L.begin(),L.end());L.erase(unique(L.begin(),L.end()),L.end());assert(L.size()==400);
 auto nullity=[&](B mask){B piv[400]{};bool has[400]{};int rank=0,count=0;
  for(int t=0;t<7;t++){U z=mask[t];while(z){int j=64*t+__builtin_ctzll(z);z&=z-1;count++;
   B v=A[j];while(true){int hi=-1;for(int c=6;c>=0;c--)if(v[c]){hi=64*c+63-__builtin_clzll(v[c]);break;}
    if(hi<0)break;
    if(!has[hi]){has[hi]=true;piv[hi]=v;rank++;break;}
    for(int c=0;c<7;c++)v[c]^=piv[hi][c];
   }
  }}return pair<int,int>(count,count-rank);
 };
 map<pair<int,int>,long long> hist;long long tested=0,exceptions=0;auto start=chrono::steady_clock::now();
 for(int i=1;i<400;i++)for(int j=i+1;j<400;j++){
  B Q{};for(int t=0;t<7;t++)Q[t]=L[0][t]|L[i][t]|L[j][t];
  for(int k=j+1;k<400;k++){
   B z{};for(int t=0;t<7;t++)z[t]=Q[t]|L[k][t];
   auto [n,d]=nullity(z);hist[{n,d}]++;tested++;
   if(d!=3){exceptions++;if(exceptions<=10)cerr<<"EXCEPTION "<<i<<" "<<j<<" "<<k<<" union="<<n<<" nullity="<<d<<"\n";}
  }
 }
 cout<<"FIXED_LINE_QUADRUPLES "<<tested<<" exceptions="<<exceptions<<" time="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"s\n";
 for(auto [p,n]:hist)cout<<"union_size="<<p.first<<" nullity="<<p.second<<" count="<<n<<"\n";
 assert(tested==10507399);
 assert(hist[make_pair(28,3)]==9604);
 assert(hist[make_pair(29,3)]==340536);
 assert(hist[make_pair(30,3)]==1775368);
 assert(hist[make_pair(31,3)]==4148928);
 assert(hist[make_pair(32,3)]==4232963);
 return exceptions?1:0;
}
