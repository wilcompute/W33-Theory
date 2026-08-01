#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
struct Shard{int a,b;};
int main(int ac,char**av){
 if(ac!=3){std::cerr<<"usage: syndrome_columns second_smallest_cutoff\n";return 2;}
 int B=std::stoi(av[2]);std::array<uint64_t,240>c{};std::ifstream in(av[1]);for(auto&x:c)if(!(in>>x))return 3;
 std::vector<Shard>s;for(int b=2;b<=B;b++)for(int a=1;a<b;a++)s.push_back({a,b});
 uint64_t expect=0;for(auto z:s)for(int d=z.b+1;d<238;d++)for(int e=d+1;e<239;e++)for(int f=e+1;f<240;f++)expect++;
 std::vector<uint64_t>v;v.reserve(expect);
 for(size_t id=0;id<s.size();id++){auto z=s[id];uint64_t base=c[0]^c[z.a]^c[z.b];for(int d=z.b+1;d<238;d++)for(int e=d+1;e<239;e++)for(int f=e+1;f<240;f++)v.push_back(((base^c[d]^c[e]^c[f])<<5)|id);}
 std::sort(v.begin(),v.end());int n=s.size();std::vector<unsigned long long>sg(n*n),ce(n*n),ds(n*n),rec(n),uni(n),dg(n),de(n),dd(n);uint64_t groups=0,multi=0;
 for(size_t i=0;i<v.size();){uint64_t syn=v[i]>>5;size_t j=i;std::array<uint32_t,32>cnt{};int active=0;while(j<v.size()&&(v[j]>>5)==syn){int q=v[j]&31;if(cnt[q]++==0)active++;j++;}groups++;if(active>1)multi++;for(int q=0;q<n;q++)if(cnt[q]){rec[q]+=cnt[q];if(cnt[q]==1)uni[q]++;}for(int a=0;a<n;a++)if(cnt[a])for(int b=a+1;b<n;b++)if(cnt[b]){sg[a*n+b]++;ce[a*n+b]+=(unsigned long long)cnt[a]*cnt[b];ds[a*n+b]+=(cnt[a]==1)+(cnt[b]==1);}i=j;}
 for(int a=0;a<n;a++)for(int b=a+1;b<n;b++){dg[a]+=sg[a*n+b];dg[b]+=sg[a*n+b];de[a]+=ce[a*n+b];de[b]+=ce[a*n+b];dd[a]+=ds[a*n+b];dd[b]+=ds[a*n+b];}
 std::cout<<"n="<<n<<" records="<<v.size()<<" syndrome_groups="<<groups<<" multishard_groups="<<multi<<"\nVERTICES\n";
 for(int q=0;q<n;q++)std::cout<<q<<" "<<s[q].a<<" "<<s[q].b<<" "<<rec[q]<<" "<<uni[q]<<" "<<dg[q]<<" "<<de[q]<<" "<<dd[q]<<"\n";
 std::cout<<"EDGES\n";for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)if(sg[a*n+b])std::cout<<a<<" "<<b<<" "<<sg[a*n+b]<<" "<<ce[a*n+b]<<" "<<ds[a*n+b]<<"\n";
}
