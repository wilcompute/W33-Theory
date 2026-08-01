#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>
struct Bits{uint64_t x[4];};
static inline bool has(const Bits&a,int i){return(a.x[i>>6]>>(i&63))&1;}
static inline void clr(Bits&a,int i){a.x[i>>6]&=~(1ULL<<(i&63));}
static inline int cntand(const Bits&a,const Bits&b){return std::popcount(a.x[0]&b.x[0])+std::popcount(a.x[1]&b.x[1])+std::popcount(a.x[2]&b.x[2])+std::popcount(a.x[3]&b.x[3]);}
std::array<uint64_t,240> col;std::array<Bits,45> inc;uint64_t C[240][5];std::vector<uint16_t> degree10;uint64_t nodes=0,codewords=0;int support_[10];
static inline uint64_t rank4(int a,int b,int c,int d){--a;--b;--c;--d;return C[a][1]+C[b][2]+C[c][3]+C[d][4];}
void leaf(){codewords++;for(int a=1;a<7;a++)for(int b=a+1;b<8;b++)for(int c=b+1;c<9;c++)for(int d=c+1;d<10;d++)degree10[rank4(support_[a],support_[b],support_[c],support_[d])]++;}
void dfs(uint64_t odd,Bits avail,int used){nodes++;int rem=10-used;if(!rem){if(!odd)leaf();return;}int no=std::popcount(odd);if(no>3*rem||((no&1)!=(rem&1)))return;if(odd){int vb=-1,cb=999;for(uint64_t z=odd;z;z&=z-1){int v=std::countr_zero(z),c=cntand(avail,inc[v]);if(!c)return;if(c<cb){cb=c;vb=v;}}Bits work=avail;for(int e=0;e<240;e++)if(has(work,e)&&has(inc[vb],e)){Bits next=work;clr(next,e);support_[used]=e;dfs(odd^col[e],next,used+1);clr(work,e);}}else{Bits work=avail;for(int e=0;e<240;e++)if(has(work,e)){Bits next=work;clr(next,e);support_[used]=e;dfs(col[e],next,used+1);clr(work,e);}}}
int main(int argc,char**argv){if(argc<4){std::cerr<<"usage: worker syndrome_columns.txt degree.bin summary.json\n";return 2;}std::ifstream in(argv[1]);for(auto &x:col)if(!(in>>x))return 3;for(auto &b:inc)b={{0,0,0,0}};for(int e=0;e<240;e++)for(int v=0;v<45;v++)if((col[e]>>v)&1)inc[v].x[e>>6]|=1ULL<<(e&63);for(int n=0;n<240;n++){C[n][0]=1;for(int k=1;k<=4;k++)C[n][k]=n?C[n-1][k]+C[n-1][k-1]:0;}degree10.assign(C[239][4],0);support_[0]=0;Bits a={{~0ULL,~0ULL,~0ULL,(1ULL<<48)-1}};clr(a,0);dfs(col[0],a,1);if(codewords!=730140)return 4;uint64_t incid=0,incident=0,maxd=0;std::map<int,uint64_t> hist;for(auto x:degree10){hist[x]++;incid+=x;if(x){incident++;maxd=std::max<uint64_t>(maxd,x);}}if(incid!=codewords*126)return 5;std::ofstream bin(argv[2],std::ios::binary);bin.write((char*)degree10.data(),degree10.size()*sizeof(uint16_t));std::ofstream o(argv[3]);o<<"{\"status\":\"PASS\",\"fixed_codewords\":"<<codewords<<",\"nodes\":"<<nodes<<",\"fixed_incident_errors\":"<<incident<<",\"fixed_incidences\":"<<incid<<",\"max_degree\":"<<maxd<<",\"global_incident_errors\":"<<incident*48<<",\"global_edges\":"<<incid*24<<",\"histogram\":{";bool first=true;for(auto [d,n]:hist){if(!first)o<<",";first=false;o<<"\""<<d<<"\":"<<n;}o<<"}}\n";std::cout<<"PASS weight10 degree: nodes="<<nodes<<" max="<<maxd<<"\n";}
