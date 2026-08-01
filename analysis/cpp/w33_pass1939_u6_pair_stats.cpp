#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
int main(int ac,char**av){if(ac!=3)return 2;int B=std::stoi(av[2]);std::array<uint64_t,240>c{};std::ifstream in(av[1]);for(auto&x:c)if(!(in>>x))return 3;uint64_t rec=0,g=0,sing=0,edges=0;int nsh=0;for(int b=2;b<=B;b++)for(int a=1;a<b;a++){std::vector<uint64_t>v;for(int d=b+1;d<238;d++)for(int e=d+1;e<239;e++)for(int f=e+1;f<240;f++)v.push_back(c[0]^c[a]^c[b]^c[d]^c[e]^c[f]);std::sort(v.begin(),v.end());rec+=v.size();nsh++;for(size_t i=0;i<v.size();){size_t j=i+1;while(j<v.size()&&v[j]==v[i])j++;auto m=j-i;g++;if(m==1)sing++;edges+=m*(m-1)/2;i=j;}}std::cout<<"shards="<<nsh<<" records="<<rec<<" independent_groups="<<g<<" independent_singletons="<<sing<<" independent_collision_edges="<<edges<<"\n";}
