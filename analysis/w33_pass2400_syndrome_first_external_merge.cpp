// Pass 2400: exact syndrome-first external merge for fixed-coordinate U6 shards.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using u64 = std::uint64_t;
using u128 = unsigned __int128;
static std::string decimal(u128 x) {
    if (!x) return "0";
    std::string s;
    while (x) { s.push_back(char('0' + x % 10)); x /= 10; }
    std::reverse(s.begin(), s.end()); return s;
}
int main(int argc, char **argv) {
    const int B = argc > 1 ? std::atoi(argv[1]) : 8;
    const std::string cols_path = argc > 2 ? argv[2] : "data/w33_pass1848_syndrome_columns.txt";
    const std::string scratch = argc > 3 ? argv[3] : "/tmp/w33_pass2400_bins";
    if (B < 2 || B > 16) throw std::runtime_error("B must lie in [2,16]");
    std::ifstream in(cols_path); if (!in) throw std::runtime_error("cannot open syndrome columns");
    std::array<u64,240> c{}; for (auto &x:c) if (!(in >> x)) throw std::runtime_error("need 240 columns");
    std::filesystem::remove_all(scratch); std::filesystem::create_directories(scratch);
    std::array<std::ofstream,256> out;
    for (int z=0; z<256; ++z) {
        char p[512]; std::snprintf(p,sizeof(p),"%s/%03d.bin",scratch.c_str(),z);
        out[z].open(p,std::ios::binary); if (!out[z]) throw std::runtime_error("cannot open radix bucket");
    }
    constexpr int SHARD_BITS=7; constexpr u64 SHARD_MASK=(u64(1)<<SHARD_BITS)-1;
    u64 records=0; int shard=0;
    for (int b=2; b<=B; ++b) for (int a=1; a<b; ++a,++shard) {
        const u64 base=c[0]^c[a]^c[b];
        for (int d=b+1; d<238; ++d) for (int e=d+1; e<239; ++e) {
            const u64 x=base^c[d]^c[e];
            for (int f=e+1; f<240; ++f) {
                const u64 syn=x^c[f];
                const u64 key=(syn<<SHARD_BITS)|u64(shard);
                const unsigned bin=unsigned((syn>>(45-8))&255u);
                out[bin].write(reinterpret_cast<const char*>(&key),sizeof(key)); ++records;
            }
        }
    }
    if (shard >= (1<<SHARD_BITS)) throw std::runtime_error("shard packing overflow");
    for (auto &o:out) o.close();
    u64 groups=0,singletons=0,maxmult=0,nonempty_bins=0,max_bin=0;
    u128 collisions=0,within=0,cross=0,shared_pair=0;
    for (int z=0; z<256; ++z) {
        char p[512]; std::snprintf(p,sizeof(p),"%s/%03d.bin",scratch.c_str(),z);
        std::ifstream fi(p,std::ios::binary|std::ios::ate); const auto bytes=fi.tellg(); fi.seekg(0);
        const std::size_t n=std::size_t(bytes)/sizeof(u64); if (!n) continue;
        ++nonempty_bins; max_bin=std::max<u64>(max_bin,n);
        std::vector<u64> v(n); fi.read(reinterpret_cast<char*>(v.data()),bytes); fi.close(); std::sort(v.begin(),v.end());
        std::size_t i=0;
        while (i<n) {
            const u64 syn=v[i]>>SHARD_BITS; std::size_t j=i; u64 total=0; int distinct=0; u128 w=0;
            while (j<n && (v[j]>>SHARD_BITS)==syn) {
                const int s=int(v[j]&SHARD_MASK); std::size_t k=j+1;
                while (k<n && (v[k]>>SHARD_BITS)==syn && int(v[k]&SHARD_MASK)==s) ++k;
                const u64 q=k-j; total+=q; w+=u128(q)*(q-1)/2; ++distinct; j=k;
            }
            ++groups; if (total==1) ++singletons; maxmult=std::max(maxmult,total);
            const u128 all=u128(total)*(total-1)/2; collisions+=all; within+=w; cross+=all-w;
            shared_pair+=u128(distinct)*(distinct-1)/2; i=j;
        }
    }
    std::cout << "{\n"
      << "  \"B\": " << B << ",\n  \"shards\": " << shard << ",\n  \"records\": " << records
      << ",\n  \"syndrome_groups\": " << groups << ",\n  \"singletons\": " << singletons
      << ",\n  \"maximum_multiplicity\": " << maxmult
      << ",\n  \"collision_edges\": " << decimal(collisions)
      << ",\n  \"within_shard_collision_edges\": " << decimal(within)
      << ",\n  \"cross_shard_collision_edges\": " << decimal(cross)
      << ",\n  \"shared_syndrome_pair_incidences\": " << decimal(shared_pair)
      << ",\n  \"radix_bins_nonempty\": " << nonempty_bins
      << ",\n  \"largest_bin_records\": " << max_bin << "\n}\n";
    return 0;
}
