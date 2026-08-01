#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
struct Tri { uint64_t s; uint16_t a,b,c; bool operator<(Tri const&o)const{return s<o.s;} };
struct Mask { array<uint64_t,4>w{}; bool operator==(Mask const&o)const{return w==o.w;} bool operator<(Mask const&o)const{return w<o.w;} };
struct MH { size_t operator()(Mask const&m)const noexcept { uint64_t h=1469598103934665603ULL; for(auto x:m.w){h^=x;h*=1099511628211ULL;}return (size_t)h;} };
static inline void setb(Mask& m,int i){m.w[i>>6]|=1ULL<<(i&63);} 
static inline bool has(Mask const&m,int i){return (m.w[i>>6]>>(i&63))&1ULL;}
static inline int pop(Mask const&m){return __builtin_popcountll(m.w[0])+__builtin_popcountll(m.w[1])+__builtin_popcountll(m.w[2])+__builtin_popcountll(m.w[3]);}
static inline bool disjoint(Tri const&x,Tri const&y){return x.a!=y.a&&x.a!=y.b&&x.a!=y.c&&x.b!=y.a&&x.b!=y.b&&x.b!=y.c&&x.c!=y.a&&x.c!=y.b&&x.c!=y.c;}
static inline Mask union6(Tri const&x,Tri const&y){Mask m;setb(m,x.a);setb(m,x.b);setb(m,x.c);setb(m,y.a);setb(m,y.b);setb(m,y.c);return m;}
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: worker syndromes240.txt frames540.txt\n";return 1;}
 vector<uint64_t> col(240); {ifstream f(argv[1]);for(auto &x:col)f>>x;}
 vector<array<int,4>> frames(540);{ifstream f(argv[2]);for(auto&r:frames)f>>r[0]>>r[1]>>r[2]>>r[3];}
 vector<Tri> t; t.reserve(2275280);
 for(int i=0;i<238;i++)for(int j=i+1;j<239;j++)for(int k=j+1;k<240;k++)t.push_back({col[i]^col[j]^col[k],(uint16_t)i,(uint16_t)j,(uint16_t)k});
 sort(t.begin(),t.end());
 uint64_t equal_pairs=0,disjoint_pairs=0; map<int,uint64_t> mult_hist;
 unordered_set<Mask,MH> c6; c6.reserve(100000);
 for(size_t l=0;l<t.size();){size_t r=l+1;while(r<t.size()&&t[r].s==t[l].s)r++;int n=r-l;mult_hist[n]++;
   equal_pairs+=(uint64_t)n*(n-1)/2;
   for(size_t i=l;i<r;i++)for(size_t j=i+1;j<r;j++)if(disjoint(t[i],t[j])){disjoint_pairs++;Mask m=union6(t[i],t[j]);if(pop(m)!=6){cerr<<"bad\n";return 2;}c6.insert(m);}l=r;}
 cerr<<"triples "<<t.size()<<" equalpairs "<<equal_pairs<<" disjointpairs "<<disjoint_pairs<<" c6 "<<c6.size()<<"\n";
 if(disjoint_pairs!=10ULL*c6.size()){cerr<<"decomp mismatch\n";return 3;}
 map<int,uint64_t> frame_contain_hist;
 vector<Mask> c6v(c6.begin(),c6.end());sort(c6v.begin(),c6v.end());
 for(auto const&m:c6v){int n=0;for(auto const&f:frames)if(has(m,f[0])&&has(m,f[1])&&has(m,f[2])&&has(m,f[3]))n++;frame_contain_hist[n]++;}
 struct Rec{Mask m;uint16_t a;bool operator<(Rec const&o)const{return m<o.m||(!(o.m<m)&&a<o.a);}};
 vector<Rec> recs; recs.reserve(540*236+c6v.size()*6);
 for(auto const&f:frames){Mask d;for(int x:f)setb(d,x);for(int a=0;a<240;a++)if(!has(d,a)){Mask e=d;setb(e,a);recs.push_back({e,(uint16_t)a});}}
 for(auto const&d:c6v)for(int a=0;a<240;a++)if(has(d,a)){Mask e=d;e.w[a>>6]^=1ULL<<(a&63);recs.push_back({e,(uint16_t)a});}
 sort(recs.begin(),recs.end());
 uint64_t distinct5=0;map<int,uint64_t> singleton_mult_hist;size_t z=0;
 while(z<recs.size()){size_t q=z+1;while(q<recs.size()&&!(recs[z].m<recs[q].m)&&!(recs[q].m<recs[z].m))q++;int cnt=0;uint16_t last=65535;for(size_t u=z;u<q;u++)if(recs[u].a!=last){cnt++;last=recs[u].a;}distinct5++;singleton_mult_hist[cnt]++;z=q;}
 auto printmap=[&](auto const&mp){cout<<"{";bool first=true;for(auto const&kv:mp){if(!first)cout<<",";first=false;cout<<"\""<<kv.first<<"\":"<<kv.second;}cout<<"}";};
 uint64_t total5=1;for(int i=0;i<5;i++)total5=total5*(240-i)/(i+1);
 uint64_t A4=540,A6=c6.size();
 unsigned long long coll4=A4*3ULL*(236ULL*235ULL*234ULL/6ULL);
 unsigned long long coll6=A6*10ULL*(234ULL*233ULL/2ULL);
 unsigned long long shadow1inc=A4*236ULL+A6*6ULL;
 unsigned long long shadow3known=A4*4ULL*(236ULL*235ULL/2ULL)+A6*15ULL*234ULL;
 cout<<"{\"schema\":\"w33.pass1838.weight5_dependency_frontier.v1\",\"status\":\"PASS\","
     <<"\"triple_count\":"<<t.size()<<",\"triple_syndrome_multiplicity\":";printmap(mult_hist);
 cout<<",\"equal_syndrome_triple_pairs\":"<<equal_pairs<<",\"disjoint_equal_triple_pairs\":"<<disjoint_pairs
     <<",\"weight6_codewords\":"<<A6<<",\"weight6_decompositions_per_codeword\":10,\"weight6_frame_containment\":";printmap(frame_contain_hist);
 cout<<",\"weight5_total\":"<<total5<<",\"weight5_singleton_shadow_incidence\":"<<shadow1inc
     <<",\"weight5_distinct_singleton_shadowed\":"<<distinct5<<",\"singleton_shadow_multiplicity\":";printmap(singleton_mult_hist);
 cout<<",\"known_weight5_collision_edges_from_A4\":"<<coll4<<",\"known_weight5_collision_edges_from_A6\":"<<coll6
     <<",\"known_weight3_shadow_incidences_from_A4_A6\":"<<shadow3known
     <<",\"boundary\":\"The exact weight-five unique-decoder coefficient additionally requires the weight-8 and weight-10 dependency atlas and overlap-degree deduplication. No coefficient or threshold is claimed here.\"}\n";
}
