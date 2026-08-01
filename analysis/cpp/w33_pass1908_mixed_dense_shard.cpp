#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <omp.h>
using Row=std::array<std::uint64_t,4>;
struct Orbit{std::uint32_t representative,size;};
static constexpr int NR=21,NP=181,NH=41;
static constexpr std::size_t NB=(std::size_t)NR*NP*NH;
static inline int pc(const Row&a,const Row&m){return std::popcount(a[0]&m[0])+std::popcount(a[1]&m[1])+std::popcount(a[2]&m[2])+std::popcount(a[3]&m[3]);}
static inline std::size_t idx(int r,int p,int h){return((std::size_t)r*NP+p)*NH+h;}
int main(int ac,char**av){
 if(ac!=7){std::cerr<<"usage ROWS ORBITS DENSE SUMMARY START STOP\n";return 2;}
 std::array<Row,45>rows{};std::ifstream ri(av[1]);for(auto&r:rows)for(auto&x:r)ri>>std::hex>>x;if(!ri)return 3;
 std::vector<Orbit>orbits;std::ifstream oi(av[2]);Orbit o{};while(oi>>o.representative>>o.size)orbits.push_back(o);if(orbits.size()!=156)return 4;
 int start=std::atoi(av[5]),stop=std::atoi(av[6]);if(start<0||stop<start||stop>(int)orbits.size())return 5;
 Row mr{0,0,0,0},mp{0,0,0,0},mh{0,0,0,0};
 for(int e=0;e<240;e++){int fw=0,rw=0;for(int i=0;i<30;i++)fw+=(rows[i][e>>6]>>(e&63))&1;for(int i=30;i<45;i++)rw+=(rows[i][e>>6]>>(e&63))&1;Row*t=nullptr;if(fw==0&&rw==3)t=&mr;else if(fw==2&&rw==1)t=&mp;else if(fw==3&&rw==0)t=&mh;else return 6;(*t)[e>>6]|=1ULL<<(e&63);}
 if(pc(mr,mr)!=20||pc(mp,mp)!=180||pc(mh,mh)!=40)return 7;
 constexpr int lb=24,hb=6;constexpr std::uint64_t lc=1ULL<<lb;
 int nt=omp_get_max_threads();std::vector<std::vector<std::uint32_t>>local(nt,std::vector<std::uint32_t>(NB));std::vector<unsigned long long>global(NB);
 double t0=omp_get_wtime();
 for(int z=start;z<stop;z++){
  for(auto&v:local)std::fill(v.begin(),v.end(),0);
  Row residual{0,0,0,0};auto cur=orbits[z];for(int b=0;b<15;b++)if((cur.representative>>b)&1U)for(int k=0;k<4;k++)residual[k]^=rows[30+b][k];
  #pragma omp parallel for schedule(dynamic,1)
  for(int high=0;high<(1<<hb);high++){
   int tid=omp_get_thread_num();Row word=residual;for(int b=0;b<hb;b++)if((high>>b)&1)for(int k=0;k<4;k++)word[k]^=rows[lb+b][k];auto&h=local[tid];
   h[idx(pc(word,mr),pc(word,mp),pc(word,mh))]++;
   for(std::uint64_t step=1;step<lc;step++){int b=std::countr_zero(step);for(int k=0;k<4;k++)word[k]^=rows[b][k];h[idx(pc(word,mr),pc(word,mp),pc(word,mh))]++;}
  }
  for(auto&v:local)for(std::size_t i=0;i<NB;i++)global[i]+=(unsigned long long)cur.size*v[i];
 }
 unsigned long long total=0,bins=0,expected=0;for(auto v:global){total+=v;bins+=v!=0;}for(int z=start;z<stop;z++)expected+=(unsigned long long)orbits[z].size*(1ULL<<30);if(total!=expected)return 8;
 std::ofstream raw(av[3],std::ios::binary);raw.write((char*)global.data(),global.size()*sizeof(global[0]));if(!raw)return 9;
 std::ofstream out(av[4]);out<<"{\"schema\":\"w33.pass1908.mixed_dense_shard.v1\",\"status\":\"PASS\",\"orbit_range\":["<<start<<","<<stop<<"],\"weighted_words\":"<<total<<",\"nonzero_bins\":"<<bins<<",\"elapsed_seconds\":"<<(omp_get_wtime()-t0)<<"}\n";
 std::cerr<<"PASS shard "<<start<<":"<<stop<<" words="<<total<<" bins="<<bins<<" elapsed="<<(omp_get_wtime()-t0)<<"\n";
 return 0;
}
