#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
constexpr int NR=540,RW=9;
struct Key{array<uint64_t,RW>w{};bool operator==(Key const&o)const{return w==o.w;}bool operator<(Key const&o)const{return w<o.w;}};
struct Hash{size_t operator()(Key const&k)const noexcept{uint64_t h=0x9e3779b97f4a7c15ULL;for(auto x:k.w){x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;x^=x>>31;h^=x+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);}return h;}};
Key transform(const Key&k,const vector<int>&g){Key y;for(int w=0;w<RW;w++){uint64_t x=k.w[w];while(x){int b=__builtin_ctzll(x);x&=x-1;int r=64*w+b;if(r<NR){int s=g[r];y.w[s/64]|=1ULL<<(s%64);}}}return y;}
vector<int> rows(const Key&k){vector<int>v;for(int w=0;w<RW;w++){uint64_t x=k.w[w];while(x){int b=__builtin_ctzll(x);x&=x-1;int r=64*w+b;if(r<NR)v.push_back(r);}}return v;}
vector<Key> load(const char*path){ifstream bin(path,ios::binary);uint64_t n=0;bin.read((char*)&n,8);vector<Key>v(n);for(auto&k:v)bin.read((char*)k.w.data(),RW*8);if(!bin)throw runtime_error("bad binary");return v;}
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: instance forward.bin reverse.bin\n";return 2;}
 ifstream in(argv[1]);int nr,nc,ng,z;in>>nr>>nc>>ng;if(nr!=NR)return 3;for(int i=0;i<nr*4;i++)in>>z;vector<vector<int>>gens(ng,vector<int>(NR));for(auto&g:gens)for(int&i:g)in>>i;
 auto forward=load(argv[2]),reverse=load(argv[3]);
 unordered_set<Key,Hash> sf,sr;sf.reserve(2*forward.size());sr.reserve(2*reverse.size());for(auto&k:forward)sf.insert(k);for(auto&k:reverse)sr.insert(k);
 uint64_t overlap=0;for(auto&k:sf)if(sr.count(k))overlap++;
 vector<Key> all=forward;all.insert(all.end(),reverse.begin(),reverse.end());sort(all.begin(),all.end());all.erase(unique(all.begin(),all.end()),all.end());
 unordered_map<Key,uint8_t,Hash> marked;marked.reserve(2*all.size());for(auto&k:all)marked.emplace(k,0);
 struct Rec{int os,st,hf,hr;Key canon;};vector<Rec>recs;uint64_t marked_n=0,total=0;
 for(auto&seed:all){if(marked[seed])continue;unordered_set<Key,Hash>seen;seen.reserve(40000);vector<Key>q{seed};seen.insert(seed);Key canon=seed;size_t head=0;int hf=0,hr=0;
  while(head<q.size()){Key x=q[head++];if(x<canon)canon=x;if(x.w[0]&1ULL){auto it=marked.find(x);if(it!=marked.end()&&!it->second){it->second=1;marked_n++;}if(sf.count(x))hf++;if(sr.count(x))hr++;}for(auto&g:gens){Key y=transform(x,g);if(seen.insert(y).second)q.push_back(y);}}
  int os=(int)q.size(),st=25920/os;total+=os;recs.push_back({os,st,hf,hr,canon});
 }
 sort(recs.begin(),recs.end(),[](const Rec&a,const Rec&b){return a.canon<b.canon;});
 map<int,int>orders;for(auto&r:recs)orders[r.st]++;
 bool pass=overlap==0&&marked_n==all.size();for(auto&r:recs)pass=pass&&r.hf>0&&r.hr>0;
 cout<<"{\"status\":\""<<(pass?"PASS":"FAIL")<<"\",\"forward_size\":"<<forward.size()<<",\"reverse_size\":"<<reverse.size()<<",\"raw_overlap\":"<<overlap<<",\"union_size\":"<<all.size()<<",\"union_marked\":"<<marked_n<<",\"distinct_full_orbits\":"<<recs.size()<<",\"certified_cover_lower_bound\":"<<total<<",\"stabilizer_order_histogram\":{";bool first=true;for(auto [k,v]:orders){if(!first)cout<<",";first=false;cout<<"\""<<k<<"\":"<<v;}cout<<"},\"orbits\":[";
 for(size_t i=0;i<recs.size();i++){if(i)cout<<",";auto&r=recs[i];auto rs=rows(r.canon);cout<<"{\"orbit_size\":"<<r.os<<",\"stabilizer_order\":"<<r.st<<",\"forward_hits\":"<<r.hf<<",\"reverse_hits\":"<<r.hr<<",\"canonical_representative\":[";for(size_t j=0;j<rs.size();j++){if(j)cout<<",";cout<<rs[j];}cout<<"]}";}cout<<"]}\n";return pass?0:1;
}
