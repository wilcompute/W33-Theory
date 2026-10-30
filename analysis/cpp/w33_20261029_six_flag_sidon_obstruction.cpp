// Exhaustive six-flag Sidon-label obstruction for the SPECIFIC design family.
// We require 7 distinct label states (including 0), mutual Hamming distance >=3,
// and unique pair XORs (unordered pair errors must be location-distinguishable).
// A label set can be translated to contain 0; search ordered subsets of F2^6.
// Compile: g++ -std=c++20 -O3 -o sidon6 analysis/cpp/w33_20261029_six_flag_sidon_obstruction.cpp
#include <bits/stdc++.h>
using namespace std;
long long nodes=0;vector<int>S{0},solution;
bool dfs(int minx,int target,uint64_t D){
 nodes++;
 if((int)S.size()==target){solution=S;return true;}
 for(int x=minx;x<64;x++){
  uint64_t e=0;bool ok=true;
  for(int y:S){
   int v=x^y;
   if(__builtin_popcount((unsigned)v)<3 || ((D>>v)&1) || ((e>>v)&1)){
    ok=false;break;
   }
   e|=1ULL<<v;
  }
  if(!ok)continue;
  S.push_back(x);
  if(dfs(x+1,target,D|e))return true;
  S.pop_back();
 }
 return false;
}
int main(){
 for(int k: {7,6,5}){
  nodes=0;S={0};solution.clear();
  bool found=dfs(1,k,0);
  cout<<"label_count="<<k<<" found="<<found<<" search_nodes="<<nodes;
  for(int x:solution)cout<<" "<<x;
  cout<<"\n";
  if(k==7)assert(!found);
  if(k==6)assert(!found);
  if(k==5)assert(found);
 }
 // Scope: no 7-element 6-bit label set obeys these specific properties,
 // NOT a general no-go on all 6-flag fault-tolerant circuits.
}
