#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
int main(int ac,char**av){if(ac!=3)return 2;std::array<std::uint64_t,240>c{};std::ifstream in(av[1]);for(auto&x:c)if(!(in>>x))return 3;std::vector<std::uint64_t>v;v.reserve(2190670);for(int d=3;d<238;d++)for(int e=d+1;e<239;e++)for(int f=e+1;f<240;f++)v.push_back(c[0]^c[1]^c[2]^c[d]^c[e]^c[f]);if(v.size()!=2190670)return 4;std::sort(v.begin(),v.end());std::uint64_t groups=0,single=0,maxm=0,coll_edges=0;for(size_t i=0;i<v.size();){size_t j=i+1;while(j<v.size()&&v[j]==v[i])j++;auto m=j-i;groups++;if(m==1)single++;maxm=std::max<std::uint64_t>(maxm,m);coll_edges+=m*(m-1)/2;i=j;}std::ofstream raw(av[2],std::ios::binary);raw.write((char*)v.data(),v.size()*8);std::cout<<"records="<<v.size()<<" groups="<<groups<<" singleton="<<single<<" max_multiplicity="<<maxm<<" collision_edges="<<coll_edges<<"\n";}
