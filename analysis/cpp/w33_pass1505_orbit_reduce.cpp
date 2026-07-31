#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
constexpr int NR=540,RW=9;
struct Key{array<uint64_t,RW>w{};bool operator==(Key const&o)const{return w==o.w;}};
struct Hash{size_t operator()(Key const&k)const noexcept{uint64_t h=0x9e3779b97f4a7c15ULL;for(auto x:k.w){x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;x^=x>>31;h^=x+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);}return h;}};
Key transform(const Key&k,const vector<int>&g){Key y;for(int w=0;w<RW;w++){uint64_t x=k.w[w];while(x){int b=__builtin_ctzll(x);x&=x-1;int r=64*w+b;if(r<NR){int s=g[r];y.w[s/64]|=1ULL<<(s%64);}}}return y;}
vector<int> rows(const Key&k){vector<int>v;for(int w=0;w<RW;w++){uint64_t x=k.w[w];while(x){int b=__builtin_ctzll(x);x&=x-1;int r=64*w+b;if(r<NR)v.push_back(r);}}return v;}
int main(int argc,char**argv){if(argc!=3)return 2;ifstream in(argv[1]);int nr,nc,ng,z;in>>nr>>nc>>ng;for(int i=0;i<nr*4;i++)in>>z;vector<vector<int>>gens(ng,vector<int>(NR));for(auto&g:gens)for(int&i:g)in>>i;ifstream bin(argv[2],ios::binary);uint64_t n;bin.read((char*)&n,8);vector<Key>sample(n);for(auto&k:sample)bin.read((char*)k.w.data(),RW*8);
 unordered_map<Key,uint8_t,Hash>mark;mark.reserve(2*n);for(auto&k:sample)mark.emplace(k,0);uint64_t classes=0,marked=0,total=0;unordered_map<int,int>orders;vector<tuple<int,int,int,vector<int>>>recs;
 for(auto&seed:sample){if(mark[seed])continue;classes++;unordered_set<Key,Hash>seen;seen.reserve(40000);vector<Key>q{seed};seen.insert(seed);size_t head=0;int hits=0;while(head<q.size()){Key x=q[head++];if(x.w[0]&1ULL){auto it=mark.find(x);if(it!=mark.end()&&!it->second){it->second=1;marked++;hits++;}}for(auto&g:gens){Key y=transform(x,g);if(seen.insert(y).second)q.push_back(y);}}int os=q.size(),st=25920/os;orders[st]++;total+=os;recs.push_back({os,st,hits,rows(seed)});}
 sort(recs.begin(),recs.end(),[](auto&a,auto&b){return get<1>(a)<get<1>(b)||(get<1>(a)==get<1>(b)&&get<3>(a)<get<3>(b));});
 cout<<"{\"status\":\""<<(marked==n?"PASS":"FAIL")<<"\",\"sample_size\":"<<n<<",\"sample_marked\":"<<marked<<",\"distinct_full_orbits\":"<<classes<<",\"certified_cover_lower_bound\":"<<total<<",\"stabilizer_order_histogram\":{";bool first=1;for(auto [k,v]:orders){if(!first)cout<<",";first=0;cout<<"\""<<k<<"\":"<<v;}cout<<"},\"orbits\":[";for(size_t i=0;i<recs.size();i++){if(i)cout<<",";auto&[os,st,hits,rs]=recs[i];cout<<"{\"orbit_size\":"<<os<<",\"stabilizer_order\":"<<st<<",\"sample_hits\":"<<hits<<",\"representative\":[";for(size_t j=0;j<rs.size();j++){if(j)cout<<",";cout<<rs[j];}cout<<"]}";}cout<<"]}\n";return marked==n?0:1;}
