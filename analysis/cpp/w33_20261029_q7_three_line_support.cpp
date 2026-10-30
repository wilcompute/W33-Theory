// Exhaustive q=7 isotropic-line union kernel rank certificate.
// Compile: g++ -O3 -std=c++20 analysis/cpp/w33_20261029_q7_three_line_support.cpp -o q7_three && ./q7_three
#include <bits/stdc++.h>
using namespace std;
using U=unsigned long long;
struct V {int x[4]; bool operator<(const V&o)const {return lexicographical_compare(x,x+4,o.x,o.x+4);} };
using B=array<U,7>;
int main(){
 set<V> ps;int q=7;
 for(int a=0;a<q;a++)for(int b=0;b<q;b++)for(int c=0;c<q;c++)for(int d=0;d<q;d++){
  int x[4]={a,b,c,d},j=0;while(j<4&&!x[j])j++; if(j==4)continue;
  int inv=1;while(inv*x[j]%q!=1)inv++;
  V v{};for(int k=0;k<4;k++)v.x[k]=x[k]*inv%q;ps.insert(v);
 }
 vector<V> p(ps.begin(),ps.end());assert(p.size()==400);
 auto form=[&](int i,int j){auto&a=p[i].x;auto&b=p[j].x;int x=a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2];return (x%q+q)%q;};
 vector<B> A(400);for(auto& a:A)a.fill(0);
 for(int i=0;i<400;i++)for(int j=0;j<400;j++)if(i!=j&&!form(i,j))A[i][j/64]|=U(1)<<(j%64);
 vector<B> L;
 for(int i=0;i<400;i++)for(int j=i+1;j<400;j++)if(A[i][j/64]>>(j%64)&1){
  B z{};for(int k=0;k<7;k++)z[k]=A[i][k]&A[j][k];
  z[i/64]|=U(1)<<(i%64);z[j/64]|=U(1)<<(j%64);L.push_back(z);
 }
 sort(L.begin(),L.end());L.erase(unique(L.begin(),L.end()),L.end());assert(L.size()==400);
 auto nul=[&](B z){B piv[400];bool has[400]={};int count=0,rr=0;
  for(int t=0;t<7;t++){U m=z[t];while(m){int j=t*64+__builtin_ctzll(m);m&=m-1;count++;
   B v=A[j];while(true){int k=-1;for(int c=6;c>=0;c--)if(v[c]){k=c*64+63-__builtin_clzll(v[c]);break;}
    if(k<0)break;
    if(!has[k]){has[k]=true;piv[k]=v;rr++;break;}
    for(int c=0;c<7;c++)v[c]^=piv[k][c];
   }
  }}
  return pair<int,int>(count,count-rr);
 };
 long long pair_hist[3][6]={},tri_hist[32][6]={};
 auto start=chrono::steady_clock::now();
 for(int i=0;i<400;i++)for(int j=i+1;j<400;j++){
  B z{};int intr=0;for(int k=0;k<7;k++){z[k]=L[i][k]|L[j][k];intr+=__builtin_popcountll(L[i][k]&L[j][k]);}
  auto [n,d]=nul(z);if(d>=6){cerr<<"pair anomaly";return 1;}pair_hist[intr][d]++;
 }
 cout<<"PAIRS ";for(int t=0;t<2;t++)for(int d=0;d<6;d++)if(pair_hist[t][d])cout<<"intersection="<<t<<" nullity="<<d<<" count="<<pair_hist[t][d]<<"; ";cout<<endl;
 long long examined=0,anomalies=0;
 for(int i=0;i<400;i++){
  for(int j=i+1;j<400;j++){
   B u{};for(int k=0;k<7;k++)u[k]=L[i][k]|L[j][k];
   for(int h=j+1;h<400;h++){
    B z{};for(int k=0;k<7;k++)z[k]=u[k]|L[h][k];
    auto [n,d]=nul(z);
    tri_hist[n][d]++;
    examined++;if(d!=2){anomalies++;if(anomalies<=10)cerr<<"ANOMALY triple "<<i<<" "<<j<<" "<<h<<" union="<<n<<" nullity="<<d<<endl;}
   }
  }
  if(i%50==0)cerr<<"progress i="<<i<<" checked="<<examined<<endl;
 }
 assert(pair_hist[0][1]==68600&&pair_hist[1][1]==11200);
 assert(examined==10586800&&anomalies==0);
 assert(tri_hist[22][2]==571200&&tri_hist[23][2]==3292800&&tri_hist[24][2]==6722800);
 cout<<"TRIPLES examined="<<examined<<" anomalous="<<anomalies<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
 for(int n=0;n<32;n++)for(int d=0;d<6;d++)if(tri_hist[n][d])cout<<"union="<<n<<" nullity="<<d<<" count="<<tri_hist[n][d]<<endl;
}
