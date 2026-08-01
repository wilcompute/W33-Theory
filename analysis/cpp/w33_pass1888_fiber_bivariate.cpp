#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
#include <omp.h>
using U=uint64_t;
int main(int argc,char**argv){if(argc<3){std::cerr<<"usage: worker rows45_hex.txt output.json\n";return 2;}std::ifstream in(argv[1]);std::array<std::array<U,4>,30>r{};std::string s;for(int i=0;i<30;i++)for(int j=0;j<4;j++){in>>s;r[i][j]=std::stoull(s,nullptr,16);}const std::array<U,4>PM={0xfefcfc71ffe3fff8ULL,0xaeaebd73bbb9dfffULL,0xbbfd7f677ade7af7ULL,0x0000b77bbbef5ddbULL};const std::array<U,4>HM={0x0101028a00140005ULL,0x4110420c40460000ULL,0x4000809885008108ULL,0x0000408404108204ULL};const uint64_t N=1ULL<<30;int nt=omp_get_max_threads();std::vector<std::vector<unsigned long long>>hist(nt,std::vector<unsigned long long>(181*41));
#pragma omp parallel
{int tid=omp_get_thread_num();uint64_t lo=N*tid/nt,hi=N*(tid+1)/nt,g=lo^(lo>>1);std::array<U,4>x={0,0,0,0};for(int b=0;b<30;b++)if((g>>b)&1)for(int k=0;k<4;k++)x[k]^=r[b][k];auto &h=hist[tid];for(uint64_t n=lo;n<hi;n++){int wp=0,wh=0;for(int k=0;k<4;k++){wp+=std::popcount(x[k]&PM[k]);wh+=std::popcount(x[k]&HM[k]);}h[wp*41+wh]++;if(n+1<hi){int b=std::countr_zero(n+1);for(int k=0;k<4;k++)x[k]^=r[b][k];}}}
std::vector<unsigned long long>H(181*41);for(auto &h:hist)for(size_t i=0;i<H.size();i++)H[i]+=h[i];uint64_t total=0,bins=0;for(auto v:H)total+=v,bins+=v>0;if(total!=N||bins!=563)return 3;for(int a=0;a<=180;a++)for(int b=0;b<=40;b++)if(H[a*41+b]!=H[a*41+40-b])return 4;std::ofstream o(argv[2]);o<<"{\"status\":\"PASS\",\"total\":"<<total<<",\"bins\":"<<bins<<",\"histogram\":[";bool first=true;for(int a=0;a<=180;a++)for(int b=0;b<=40;b++)if(H[a*41+b]){if(!first)o<<",";first=false;o<<"["<<a<<","<<b<<","<<H[a*41+b]<<"]";}o<<"]}\n";std::cout<<"PASS fiber bivariate bins="<<bins<<"\n";}
