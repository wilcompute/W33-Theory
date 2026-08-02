#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>
using u64=uint64_t;using u128=unsigned __int128;
struct Rec{u64 syn,rank;uint32_t mask;};
static u64 C[241][7];
static std::string dec(u128 x){if(!x)return"0";std::string s;while(x){s.push_back('0'+x%10);x/=10;}reverse(s.begin(),s.end());return s;}
static u64 rank5(std::array<int,5> a){u64 r=0;for(int i=0;i<5;i++)r+=C[a[i]][i+1];return r;}
int main(int argc,char**argv){if(argc!=3)return 2;int nsh=std::stoi(argv[2]);if(nsh<2||nsh>30)return 3;for(int n=0;n<=240;n++){C[n][0]=1;for(int k=1;k<=6;k++)C[n][k]=(n?C[n-1][k]+C[n-1][k-1]:0);}std::ifstream in(argv[1]);std::array<u64,240>col{};for(auto&x:col)if(!(in>>x))return 4;
 std::vector<Rec> v;v.reserve((size_t)nsh*2200000);for(int sh=0;sh<nsh;sh++){std::array<int,3>f{0,1,sh+2};std::array<bool,240>is{};for(int x:f)is[x]=1;std::vector<int> free;for(int x=0;x<240;x++)if(!is[x])free.push_back(x);u64 base=col[f[0]]^col[f[1]]^col[f[2]];
  for(int ia=0;ia<(int)free.size();ia++)for(int ib=ia+1;ib<(int)free.size();ib++)for(int ic=ib+1;ic<(int)free.size();ic++){int a=free[ia],b=free[ib],c=free[ic];std::array<int,5>q{};int z=0;for(int x:{f[1],f[2],a,b,c})q[z++]=x-1;std::sort(q.begin(),q.end());v.push_back({base^col[a]^col[b]^col[c],rank5(q),uint32_t(1u<<sh)});}}
 std::sort(v.begin(),v.end(),[](auto&a,auto&b){return a.syn<b.syn||(a.syn==b.syn&&(a.rank<b.rank||(a.rank==b.rank&&a.mask<b.mask)));});
 u64 records=v.size(),duplicate_records=0,unique_reps=0,syndrome_groups=0,singleton_groups=0,collision_groups=0,max_mult=0,multi_shard_groups=0;u128 pairs=0,cross_pairs=0;std::vector<u64> marked,all;marked.reserve(records);all.reserve(records);std::array<u64,31>shard_degree_hist{};std::array<u64,31>rep_shard_mult_hist{};
 size_t i=0;while(i<v.size()){size_t j=i;while(j<v.size()&&v[j].syn==v[i].syn)j++;syndrome_groups++;std::vector<std::pair<u64,uint32_t>>u;for(size_t k=i;k<j;){u64 r=v[k].rank;uint32_t sm=0;size_t l=k;while(l<j&&v[l].rank==r){sm|=v[l].mask;l++;}duplicate_records+=l-k-1;u.push_back({r,sm});all.push_back(r);rep_shard_mult_hist[__builtin_popcount(sm)]++;k=l;}unique_reps+=u.size();max_mult=std::max<u64>(max_mult,u.size());if(u.size()==1)singleton_groups++;else{collision_groups++;pairs+=u128(u.size())*(u.size()-1)/2;for(auto&x:u)marked.push_back(x.first);}uint32_t unionmask=0;for(auto&x:u)unionmask|=x.second;int d=__builtin_popcount(unionmask);shard_degree_hist[d]++;if(d>1)multi_shard_groups++;
  u128 tp=u128(u.size())*(u.size()-1)/2, same_single=0;std::array<u64,30> ns{};
  for(auto &x:u)if(__builtin_popcount(x.second)==1)ns[__builtin_ctz(x.second)]++;
  for(int s=0;s<nsh;s++)same_single+=u128(ns[s])*(ns[s]-1)/2;
  cross_pairs+=tp-same_single;
  i=j;}
 std::sort(marked.begin(),marked.end());marked.erase(std::unique(marked.begin(),marked.end()),marked.end());std::sort(all.begin(),all.end());all.erase(std::unique(all.begin(),all.end()),all.end());
 std::cout<<"{\n  \"schema\": \"w33.pass2470.multishard_union_demo.v1\",\n  \"shard_count\": "<<nsh<<",\n  \"fixed_triples\": [";for(int s=0;s<nsh;s++){if(s)std::cout<<",";std::cout<<"[0,1,"<<s+2<<"]";}std::cout<<"],\n  \"records\": "<<records<<",\n  \"unique_representatives\": "<<all.size()<<",\n  \"duplicate_records_removed\": "<<duplicate_records<<",\n  \"syndrome_groups\": "<<syndrome_groups<<",\n  \"singleton_distinct_groups\": "<<singleton_groups<<",\n  \"collision_groups\": "<<collision_groups<<",\n  \"maximum_distinct_multiplicity\": "<<max_mult<<",\n  \"distinct_collision_pairs\": "<<dec(pairs)<<",\n  \"cross_shard_distinct_collision_pairs\": "<<dec(cross_pairs)<<",\n  \"collision_marked_union_representatives\": "<<marked.size()<<",\n  \"collision_unmarked_union_representatives\": "<<(all.size()-marked.size())<<",\n  \"multi_shard_syndrome_groups\": "<<multi_shard_groups<<",\n  \"representative_shard_multiplicity_histogram\": {";bool f=1;for(int d=1;d<=nsh;d++)if(rep_shard_mult_hist[d]){if(!f)std::cout<<",";f=0;std::cout<<"\""<<d<<"\":"<<rep_shard_mult_hist[d];}std::cout<<"},\n  \"syndrome_shard_degree_histogram\": {";f=1;for(int d=1;d<=nsh;d++)if(shard_degree_hist[d]){if(!f)std::cout<<",";f=0;std::cout<<"\""<<d<<"\":"<<shard_degree_hist[d];}std::cout<<"}\n}\n";
}
