// Exact W(3,7) FIVE-isotropic-line union supported-kernel theorem.
// Pair-orbit reduction: the symplectic group is transitive on intersecting
// and skew ordered line pairs. Thus fix L0, one of two partner orbits,
// enumerate all choose(398,3) remaining triples in each case.
// g++ -O3 -std=c++20 analysis/cpp/w33_20261029_q7_five_line_pair_orbits.cpp -o /tmp/q7five && /tmp/q7five
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;using B=array<U,7>;
struct V{array<int,4> a;bool operator<(V const&o)const{return a<o.a;}};
int main(){const int q=7;set<V> sp;
for(int a=0;a<q;a++)for(int b=0;b<q;b++)for(int c=0;c<q;c++)for(int d=0;d<q;d++){
array<int,4>x{a,b,c,d};int k=0;while(k<4&&!x[k])k++;if(k==4)continue;int z=1;while(z*x[k]%q!=1)z++;V v;for(int j=0;j<4;j++)v.a[j]=z*x[j]%q;sp.insert(v);}
vector<V>P(sp.begin(),sp.end());assert(P.size()==400);
auto form=[&](int i,int j){auto &a=P[i].a,&b=P[j].a;int v=a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2];return(v%q+q)%q;};
vector<B>A(400);for(auto& a:A)a.fill(0);
for(int i=0;i<400;i++)for(int j=0;j<400;j++)if(i!=j&&!form(i,j))A[i][j/64]|=U(1)<<(j%64);
vector<B>L;for(int i=0;i<400;i++)for(int j=i+1;j<400;j++)if(A[i][j/64]>>(j%64)&1){B v{};for(int k=0;k<7;k++)v[k]=A[i][k]&A[j][k];v[i/64]|=U(1)<<(i%64);v[j/64]|=U(1)<<(j%64);L.push_back(v);}
sort(L.begin(),L.end());L.erase(unique(L.begin(),L.end()),L.end());assert(L.size()==400);
auto intersection=[&](int i,int j){int s=0;for(int k=0;k<7;k++)s+=__builtin_popcountll(L[i][k]&L[j][k]);return s;};
int near=-1,far=-1;for(int j=1;j<400;j++){int s=intersection(0,j);if(s==1&&near<0)near=j;else if(s==0&&far<0)far=j;}assert(near>=0&&far>=0);
auto nullity=[&](B mask){B piv[400]{};bool has[400]{};int rank=0,count=0;
for(int t=0;t<7;t++){U z=mask[t];while(z){int j=64*t+__builtin_ctzll(z);z&=z-1;count++;
B v=A[j];while(true){int hi=-1;for(int c=6;c>=0;c--)if(v[c]){hi=64*c+63-__builtin_clzll(v[c]);break;}
 if(hi<0)break;
 if(!has[hi]){has[hi]=true;piv[hi]=v;rank++;break;}
 for(int c=0;c<7;c++)v[c]^=piv[hi][c];
}
}}
return pair<int,int>(count,count-rank);
};
map<tuple<int,int,int>,long long> hist;long long tested=0,exceptions=0;auto start=chrono::steady_clock::now();
for(int typ=0;typ<2;typ++){
 int f=(typ==0?near:far);vector<int> others;for(int j=1;j<400;j++)if(j!=f)others.push_back(j);assert(others.size()==398);
 for(int ai=0;ai<398;ai++)for(int bi=ai+1;bi<398;bi++){
 B Q{};for(int t=0;t<7;t++)Q[t]=L[0][t]|L[f][t]|L[others[ai]][t]|L[others[bi]][t];
 for(int ci=bi+1;ci<398;ci++){
 B z{};for(int t=0;t<7;t++)z[t]=Q[t]|L[others[ci]][t];
 auto [n,d]=nullity(z);hist[{typ,n,d}]++;tested++;
 if(d!=4){exceptions++;if(exceptions<=12)cerr<<"EXCEPTION "<<typ<<":"<<f<<","<<others[ai]<<","<<others[bi]<<","<<others[ci]<<" union="<<n<<" nullity="<<d<<"\n";}
}
}
cout<<"DONE pair_type="<<(typ==0?"meeting":"skew")<<" examined="<<tested<<" exceptions="<<exceptions<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
}
assert(tested==2*10428396);
assert(hist[make_tuple(0,34,4)]==2058 && hist[make_tuple(0,35,4)]==86436 && hist[make_tuple(0,36,4)]==840958);
assert(hist[make_tuple(0,37,4)]==2709602 && hist[make_tuple(0,38,4)]==4124232 && hist[make_tuple(0,39,4)]==2665110);
assert(hist[make_tuple(1,34,4)]==224 && hist[make_tuple(1,35,4)]==13440 && hist[make_tuple(1,36,4)]==193224);
assert(hist[make_tuple(1,37,4)]==993296 && hist[make_tuple(1,38,4)]==2651376 && hist[make_tuple(1,39,4)]==3916080 && hist[make_tuple(1,40,4)]==2660756);
cout<<"FIVE_LINE_ORBIT_CENSUS tested="<<tested<<" exceptions="<<exceptions<<" time="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"s\n";
for(auto const& kv:hist)cout<<"type="<<get<0>(kv.first)<<" union="<<get<1>(kv.first)<<" nullity="<<get<2>(kv.first)<<" count="<<kv.second<<"\n";
return exceptions?1:0;
}