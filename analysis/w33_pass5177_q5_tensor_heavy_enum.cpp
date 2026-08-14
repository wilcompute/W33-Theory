// Pass5177 companion: exhaustive 2^25 q=5 tensor-component heavy-shell census.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <map>
#include <tuple>
#include <vector>
using namespace std;

static int cutWeight5(int msg){
    int k=__builtin_popcount((unsigned)msg);
    return k*(6-k); // 0,5,8,9 for a Cut(K6) word in the fixed-vertex gauge.
}

struct State { int w,h8,h9,active; long long count; };

int main(){
    vector<int> R;
    for(int i=0;i<5;i++)R.push_back(1<<i);
    for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)R.push_back((1<<i)|(1<<j));

    map<tuple<int,int,int,int>,long long> dist;
    for(uint32_t code=0;code<(1u<<25);code++){
        int row[5],col[5]={0};
        for(int i=0;i<5;i++)row[i]=(code>>(5*i))&31;
        for(int j=0;j<5;j++)for(int i=0;i<5;i++)if((row[i]>>j)&1)col[j]|=1<<i;
        int w=0,h8=0,h9=0,active=0;
        for(int r:R){
            int msg=0;for(int i=0;i<5;i++)if((r>>i)&1)msg^=row[i];
            int x=cutWeight5(msg);w+=x;if(x){active++;if(x==8)h8++;else if(x==9)h9++;}
        }
        for(int r:R){
            int msg=0;for(int j=0;j<5;j++)if((r>>j)&1)msg^=col[j];
            int x=cutWeight5(msg);if(x){active++;if(x==8)h8++;else if(x==9)h9++;}
        }
        dist[{w,h8,h9,active}]++;
    }
    if(dist.size()!=140)return 2;

    // Low-heavy classification: h8<=2,h9<=1.
    map<tuple<int,int,int,int>,long long> low;
    for(auto &kv:dist){auto [w,h8,h9,a]=kv.first;if(h8<=2&&h9<=1)low[kv.first]=kv.second;}
    if(low.size()!=3)return 3;
    if(low[{0,0,0,0}]!=1)return 4;
    if(low[{25,0,0,10}]!=36)return 5;
    if(low[{48,2,0,18}]!=450)return 6;
    // In particular no component can carry h9=1 while total h8<=2.

    // Unbounded knapsack over nonzero component state TYPES: at total word
    // weight 625, find the smallest positive coarea cost 3h8+4h9.
    vector<State>S;
    for(auto &kv:dist){auto [w,h8,h9,a]=kv.first;if(w)S.push_back({w,h8,h9,a,kv.second});}
    const int INF=1e9;
    vector<array<int,2>> dp(626,{INF,INF});
    vector<array<pair<int,int>,2>> par(626); // previous weight,state index
    dp[0][0]=0;
    for(int W=0;W<=625;W++)for(int flag=0;flag<2;flag++)if(dp[W][flag]<INF){
        for(int i=0;i<(int)S.size();i++){
            int nw=W+S[i].w;if(nw>625)continue;
            int c=3*S[i].h8+4*S[i].h9,nf=flag||(c>0);
            if(dp[W][flag]+c<dp[nw][nf]){
                dp[nw][nf]=dp[W][flag]+c;par[nw][nf]={W,i};
            }
        }
    }
    if(dp[625][0]!=0)return 7;
    if(dp[625][1]!=50)return 8;

    // Recover one minimum-positive-cost composition.
    vector<int> mult(S.size());int W=625,flag=1;
    while(W){auto [PW,i]=par[W][flag];if(i<0)return 9;mult[i]++;int c=3*S[i].h8+4*S[i].h9;flag=(flag && !(c>0 && dp[PW][0]+c==dp[W][1]));W=PW;}

    cout<<"{\n";
    cout<<"  \"component_states\": 33554432,\n";
    cout<<"  \"distinct_component_profiles\": 140,\n";
    cout<<"  \"low_heavy_profiles\": [\n";
    cout<<"    {\"weight\":0,\"h8\":0,\"h9\":0,\"active\":0,\"count\":1},\n";
    cout<<"    {\"weight\":25,\"h8\":0,\"h9\":0,\"active\":10,\"count\":36},\n";
    cout<<"    {\"weight\":48,\"h8\":2,\"h9\":0,\"active\":18,\"count\":450}\n";
    cout<<"  ],\n";
    cout<<"  \"minimal_exotic_2_1_possible\": false,\n";
    cout<<"  \"minimum_positive_global_coarea_cost_at_weight625\": 50,\n";
    cout<<"  \"minimum_positive_active_chart_defect\": 10,\n";
    cout<<"  \"example_minimum_composition\": [\n";
    bool first=true;
    for(int i=0;i<(int)S.size();i++)if(mult[i]){
        if(!first)cout<<",\n";first=false;
        cout<<"    {\"multiplicity\":"<<mult[i]<<",\"weight\":"<<S[i].w<<",\"h8\":"<<S[i].h8<<",\"h9\":"<<S[i].h9<<",\"active\":"<<S[i].active<<"}";
    }
    cout<<"\n  ]\n}\n";
    return 0;
}
