#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std; constexpr int RW=9;
struct K{array<uint64_t,RW>w;};
int main(int argc,char**argv){ifstream in(argv[1],ios::binary);uint32_t nt;in.read((char*)&nt,4);vector<vector<K>> F(nt);for(int i=0;i<(int)nt;i++){uint64_t n;in.read((char*)&n,8);F[i].resize(n);for(auto&x:F[i])in.read((char*)x.w.data(),RW*8);}cout<<"[";bool fst=1;for(int i=0;i<(int)nt;i++)for(int j=i+1;j<(int)nt;j++){uint64_t cnt=0;for(auto&a:F[i])for(auto&b:F[j]){uint64_t z=0;for(int k=0;k<RW;k++)z|=a.w[k]&b.w[k];cnt+=!z;}if(!fst)cout<<",";fst=0;cout<<"["<<i<<","<<j<<","<<cnt<<"]";cerr<<i<<","<<j<<"="<<cnt<<"\n";}cout<<"]\n";}
