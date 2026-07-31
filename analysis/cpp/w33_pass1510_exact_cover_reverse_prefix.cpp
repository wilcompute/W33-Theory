#include <array>
#include <chrono>
#include <climits>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
constexpr int NR=540, NC=240, RW=9, CW=4;
struct Key { array<uint64_t,RW> w{}; };
array<array<uint64_t,CW>,NR> row_cols;
array<array<uint64_t,RW>,NR> conflicts;
array<array<uint64_t,RW>,NC> col_rows;
uint64_t found=0,nodes=0,target=0; vector<Key> solutions;
inline bool all(const array<uint64_t,CW>&c){return c[0]==~0ULL&&c[1]==~0ULL&&c[2]==~0ULL&&c[3]==((1ULL<<48)-1);}
inline int candidates(int c,const array<uint64_t,RW>&a){int n=0;for(int w=0;w<RW;w++)n+=__builtin_popcountll(col_rows[c][w]&a[w]);return n;}
bool dfs(array<uint64_t,CW> covered,array<uint64_t,RW> active,Key&chosen){
 nodes++; if(found>=target)return true;
 if(all(covered)){found++;solutions.push_back(chosen);return found>=target;}
 int best=-1,bn=INT_MAX;
 for(int wi=0;wi<CW;wi++){uint64_t x=~covered[wi];if(wi==3)x&=((1ULL<<48)-1);while(x){int bit=__builtin_ctzll(x);x&=x-1;int c=64*wi+bit,n=candidates(c,active);if(!n)return false;if(n<bn){best=c;bn=n;if(n==1)goto selected;}}}
selected:
 array<uint64_t,RW> cand{};for(int w=0;w<RW;w++)cand[w]=col_rows[best][w]&active[w];
 for(int w=RW-1;w>=0;w--){uint64_t x=cand[w];while(x){int bit=63-__builtin_clzll(x);x&=~(1ULL<<bit);int r=64*w+bit;if(r>=NR)continue;auto c2=covered;for(int j=0;j<CW;j++)c2[j]|=row_cols[r][j];auto a2=active;for(int j=0;j<RW;j++)a2[j]&=~conflicts[r][j];chosen.w[r/64]|=1ULL<<(r%64);bool stop=dfs(c2,a2,chosen);chosen.w[r/64]&=~(1ULL<<(r%64));if(stop)return true;}}
 return false;
}
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: instance.txt sample_size output.bin\n";return 2;} target=stoull(argv[2]);ifstream in(argv[1]);int nr,nc,ng;in>>nr>>nc>>ng;if(nr!=NR||nc!=NC)return 3;vector<array<int,4>>rows(NR);
 for(int r=0;r<NR;r++)for(int j=0;j<4;j++){int c;in>>c;rows[r][j]=c;row_cols[r][c/64]|=1ULL<<(c%64);col_rows[c][r/64]|=1ULL<<(r%64);}int z;for(int i=0;i<ng*NR;i++)in>>z;
 for(int r=0;r<NR;r++)for(int c:rows[r])for(int w=0;w<RW;w++)conflicts[r][w]|=col_rows[c][w];
 array<uint64_t,CW>covered=row_cols[0];array<uint64_t,RW>active{};for(auto&x:active)x=~0ULL;active[8]&=((1ULL<<28)-1);for(int w=0;w<RW;w++)active[w]&=~conflicts[0][w];Key chosen;chosen.w[0]|=1ULL;
 auto t=chrono::steady_clock::now();dfs(covered,active,chosen);double sec=chrono::duration<double>(chrono::steady_clock::now()-t).count();
 ofstream out(argv[3],ios::binary);uint64_t n=solutions.size();out.write((char*)&n,sizeof(n));for(auto&k:solutions)out.write((char*)k.w.data(),RW*sizeof(uint64_t));
 cout<<"{\"status\":\""<<(found==target?"PASS":"FAIL")<<"\",\"sample_size\":"<<found<<",\"nodes\":"<<nodes<<",\"seconds\":"<<sec<<"}\n";return found==target?0:1;
}
