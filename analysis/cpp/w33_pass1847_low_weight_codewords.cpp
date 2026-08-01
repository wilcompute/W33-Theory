#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
struct Bits{uint64_t x[4];};
static inline bool has(const Bits&a,int i){return(a.x[i>>6]>>(i&63))&1;}
static inline void clr(Bits&a,int i){a.x[i>>6]&=~(1ULL<<(i&63));}
static inline int cntand(const Bits&a,const Bits&b){return std::popcount(a.x[0]&b.x[0])+std::popcount(a.x[1]&b.x[1])+std::popcount(a.x[2]&b.x[2])+std::popcount(a.x[3]&b.x[3]);}
std::array<uint64_t,240> col;std::array<Bits,45> inc;int target;unsigned long long sol,nodes;
void dfs(uint64_t odd,Bits avail,int used){nodes++;int rem=target-used;if(rem==0){sol+=odd==0;return;}int no=std::popcount(odd);if(no>3*rem||((no&1)!=(rem&1)))return;
 if(odd){int vb=-1,cb=999;for(uint64_t z=odd;z;z&=z-1){int v=std::countr_zero(z);int c=cntand(avail,inc[v]);if(!c)return;if(c<cb){cb=c;vb=v;}}
  Bits work=avail;for(int e=0;e<240;e++)if(has(work,e)&&has(inc[vb],e)){Bits next=work;clr(next,e);dfs(odd^col[e],next,used+1);clr(work,e);}}
 else{Bits work=avail;for(int e=0;e<240;e++)if(has(work,e)){Bits next=work;clr(next,e);dfs(col[e],next,used+1);clr(work,e);}}
}
unsigned long long count_weight(int w,unsigned long long &n){target=w;sol=nodes=0;Bits a={{~0ULL,~0ULL,~0ULL,(1ULL<<48)-1}};clr(a,0);dfs(col[0],a,1);n=nodes;return sol*240/w;}
int main(int argc,char**argv){if(argc<3)return 2;std::ifstream in(argv[1]);for(auto &x:col)if(!(in>>x))return 3;for(auto &b:inc)b={{0,0,0,0}};for(int e=0;e<240;e++)for(int v=0;v<45;v++)if(col[e]>>v&1)inc[v].x[e>>6]|=1ULL<<(e&63);
 std::map<int,unsigned long long>A,N,C;for(int w:{4,6,8,10})A[w]=count_weight(w,N[w]);
 C[4]=A[4]*3ULL*27730ULL;
 C[6]=A[6]*10ULL*234ULL;
 C[8]=A[8]*35ULL;
 unsigned long long eq4=C[4]+C[6]+C[8];
 unsigned long long e5_4=A[4]*3ULL*2162940ULL;
 unsigned long long e5_6=A[6]*10ULL*27261ULL;
 unsigned long long e5_8=A[8]*35ULL*232ULL;
 unsigned long long e5_10=A[10]*126ULL;
 std::ofstream o(argv[2]);o<<"{\"schema\":\"w33.pass1847.low_weight_decoder_frontier.v1\",\"status\":\"PASS\",\"A4\":"<<A[4]<<",\"A6\":"<<A[6]<<",\"A8\":"<<A[8]<<",\"A10\":"<<A[10]<<",\"fixed_coordinate_counts\":{\"4\":"<<A[4]*4/240<<",\"6\":"<<A[6]*6/240<<",\"8\":"<<A[8]*8/240<<",\"10\":"<<A[10]*10/240<<"},\"dfs_nodes\":{\"4\":"<<N[4]<<",\"6\":"<<N[6]<<",\"8\":"<<N[8]<<",\"10\":"<<N[10]<<"},\"weight4_equal_syndrome_pairs\":"<<eq4<<",\"weight5_collision_edges\":"<<(e5_4+e5_6+e5_8+e5_10)<<",\"weight5_collision_terms\":{\"A4\":"<<e5_4<<",\"A6\":"<<e5_6<<",\"A8\":"<<e5_8<<",\"A10\":"<<e5_10<<"},\"boundary\":\"A4,A6,A8,A10 and the complete weight-five collision-edge count are exact. The unique-minimum weight-five decoder coefficient still requires the collision-degree/component distribution; edge totals alone do not deduplicate ambiguous syndromes.\"}\n";
 std::cout<<"A4="<<A[4]<<" A6="<<A[6]<<" A8="<<A[8]<<" A10="<<A[10]<<" collision5="<<(e5_4+e5_6+e5_8+e5_10)<<"\n";
}
