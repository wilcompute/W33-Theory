#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <unordered_set>
#include <vector>
struct H{size_t operator()(std::uint64_t x)const noexcept{x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;x^=x>>31;return x;}};
int main(int ac,char**av){if(ac!=3)return 2;std::array<std::uint64_t,240>c{};std::ifstream in(av[1]);for(auto&x:c)if(!(in>>x))return 3;std::ifstream raw(av[2],std::ios::binary|std::ios::ate);size_t n=raw.tellg()/8;raw.seekg(0);std::vector<std::uint64_t>v(n);raw.read((char*)v.data(),n*8);std::unordered_set<std::uint64_t,H>target;target.reserve(2400000);for(size_t i=0;i<n;){target.insert(v[i]);size_t j=i+1;while(j<n&&v[j]==v[i])j++;i=j;}std::unordered_set<std::uint64_t,H>matched;matched.reserve(1000000);auto test=[&](uint64_t s){if(target.find(s)!=target.end())matched.insert(s);};test(0);for(int a=0;a<239;a++)for(int b=a+1;b<240;b++)test(c[a]^c[b]);for(int a=0;a<237;a++)for(int b=a+1;b<238;b++)for(int d=b+1;d<239;d++)for(int e=d+1;e<240;e++)test(c[a]^c[b]^c[d]^c[e]);uint64_t lower_groups=matched.size(),lower_records=0,lower_singletons=0,nonlower_singletons=0;for(size_t i=0;i<n;){size_t j=i+1;while(j<n&&v[j]==v[i])j++;bool lo=matched.count(v[i]);if(lo){lower_records+=j-i;if(j-i==1)lower_singletons++;}else if(j-i==1)nonlower_singletons++;i=j;}std::cout<<"target_groups="<<target.size()<<" matched_lower_groups="<<lower_groups<<" lower_records="<<lower_records<<" lower_singletons="<<lower_singletons<<" nonlower_singletons="<<nonlower_singletons<<"\n";}
