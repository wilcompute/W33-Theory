#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
#include <chrono>
int main(int ac,char**av){
 if(ac!=3){std::cerr<<"usage cols B\n";return 2;} int B=std::stoi(av[2]);
 std::array<std::uint64_t,240> c{}; std::ifstream in(av[1]); for(auto &x:c) if(!(in>>x)) return 3;
 std::uint64_t expect=0; for(int b=2;b<=B;b++) for(int a=1;a<b;a++) for(int d=b+1;d<238;d++) for(int e=d+1;e<239;e++) for(int f=e+1;f<240;f++) expect++;
 std::vector<std::uint64_t> v; v.reserve(expect);
 for(int b=2;b<=B;b++) for(int a=1;a<b;a++){
   auto base=c[0]^c[a]^c[b];
   for(int d=b+1;d<238;d++) for(int e=d+1;e<239;e++) for(int f=e+1;f<240;f++) v.push_back(base^c[d]^c[e]^c[f]);
 }
 if(v.size()!=expect){std::cerr<<"size mismatch\n";return 4;}
 std::sort(v.begin(),v.end());
 std::vector<std::uint64_t> u; u.reserve(v.size()); std::vector<unsigned char> singleton; singleton.reserve(v.size());
 std::uint64_t groups=0,singles=0,maxm=0,edges=0;
 for(size_t i=0;i<v.size();){size_t j=i+1;while(j<v.size()&&v[j]==v[i])j++;auto m=j-i;u.push_back(v[i]);singleton.push_back(m==1);groups++;if(m==1)singles++;maxm=std::max<std::uint64_t>(maxm,m);edges+=m*(m-1)/2;i=j;}
 std::vector<unsigned char> lower(u.size(),0);
 auto mark=[&](std::uint64_t s){auto it=std::lower_bound(u.begin(),u.end(),s);if(it!=u.end()&&*it==s)lower[it-u.begin()]=1;};
 mark(0);
 for(int a=0;a<239;a++)for(int b=a+1;b<240;b++)mark(c[a]^c[b]);
 for(int a=0;a<237;a++)for(int b=a+1;b<238;b++)for(int d=b+1;d<239;d++)for(int e=d+1;e<240;e++)mark(c[a]^c[b]^c[d]^c[e]);
 std::uint64_t lower_groups=0,lower_singletons=0,nonlower_singletons=0;
 for(size_t i=0;i<u.size();i++)if(lower[i]){lower_groups++;if(singleton[i])lower_singletons++;}else if(singleton[i])nonlower_singletons++;
 std::cout<<"B="<<B<<" records="<<v.size()<<" groups="<<groups<<" singleton_groups="<<singles<<" max_multiplicity="<<maxm<<" collision_edges="<<edges<<" lower_groups="<<lower_groups<<" lower_singletons="<<lower_singletons<<" nonlower_singletons="<<nonlower_singletons<<"\n";
}
