#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using boost::multiprecision::cpp_int;

std::vector<std::vector<cpp_int>> kraw(int n){
  std::vector<std::vector<cpp_int>> K(n+1,std::vector<cpp_int>(n+1));
  for(int x=0;x<=n;x++){
    K[0][x]=1;
    if(n>=1) K[1][x]=n-2*x;
    for(int m=1;m<n;m++){
      cpp_int z=(n-2*x)*K[m][x]-(n-m+1)*K[m-1][x];
      if(z%(m+1)!=0){std::cerr<<"bad recurrence\n";std::exit(2);} K[m+1][x]=z/(m+1);
    }
  }
  return K;
}
struct Row{int r,p,h; std::uint64_t a;};
int main(int ac,char**av){
  if(ac!=3){std::cerr<<"usage dual_sparse.txt primal_sparse.txt\n";return 2;}
  std::ifstream in(av[1]); std::vector<Row> rows; Row q;
  while(in>>q.r>>q.p>>q.h>>q.a) rows.push_back(q);
  std::cerr<<"rows="<<rows.size()<<"\n";
  auto K20=kraw(20),K180=kraw(180),K40=kraw(40);
  const int R=21,P=181,H=41; auto id=[&](int i,int p,int h){return (i*P+p)*H+h;};
  std::vector<cpp_int>B(R*P*H),C(R*P*H);
  for(auto &x:rows) for(int i=0;i<R;i++) B[id(i,x.p,x.h)]+=K20[i][x.r]*x.a;
  std::cerr<<"r transform\n";
  for(int i=0;i<R;i++) for(int h=0;h<H;h++) for(int j=0;j<P;j++){
    cpp_int s=0; for(int p=0;p<P;p++) if(B[id(i,p,h)]!=0) s+=B[id(i,p,h)]*K180[j][p]; C[id(i,j,h)]=s;
  }
  std::cerr<<"p transform\n";
  cpp_int denom=cpp_int(1)<<45, total=0; std::uint64_t nz=0;
  std::ofstream out(av[2]);
  for(int i=0;i<R;i++) for(int j=0;j<P;j++) for(int k=0;k<H;k++){
    cpp_int s=0; for(int h=0;h<H;h++) if(C[id(i,j,h)]!=0) s+=C[id(i,j,h)]*K40[k][h];
    if(s%denom!=0){std::cerr<<"nonintegral "<<i<<" "<<j<<" "<<k<<"\n";return 3;}
    s/=denom; if(s<0){std::cerr<<"negative\n";return 4;} if(s!=0){out<<i<<" "<<j<<" "<<k<<" "<<s<<"\n";total+=s;nz++;}
  }
  cpp_int expected=cpp_int(1)<<195;
  std::cerr<<"nz="<<nz<<" total_ok="<<(total==expected)<<"\n";
  return total==expected?0:5;
}
