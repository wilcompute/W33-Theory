#include <array>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
constexpr int NR = 540, NC = 240, CW = 4;
using Cols = array<uint64_t, CW>;
array<array<int, 4>, NR> rows;
array<vector<int>, NC> col_rows;
array<uint8_t, NR> forbidden{};
uint64_t nodes = 0, forced_steps = 0, dead_ends = 0;
ofstream trace_out;

static inline bool covered(const Cols& c, int j) { return (c[j >> 6] >> (j & 63)) & 1ULL; }
static inline bool compatible(int r, const Cols& c) {
    if (forbidden[r]) return false;
    for (int j : rows[r]) if (covered(c, j)) return false;
    return true;
}
static inline void add_row(int r, Cols& c) { for (int j : rows[r]) c[j >> 6] |= 1ULL << (j & 63); }
static inline bool complete(const Cols& c) {
    return c[0] == ~0ULL && c[1] == ~0ULL && c[2] == ~0ULL && c[3] == ((1ULL << 48) - 1);
}
static void trace(uint8_t tag, const Cols& c, int value) {
    trace_out.write(reinterpret_cast<const char*>(&tag), 1);
    trace_out.write(reinterpret_cast<const char*>(c.data()), CW * sizeof(uint64_t));
    trace_out.write(reinterpret_cast<const char*>(&value), sizeof(value));
}

static bool dfs(Cols cov, vector<int>& witness) {
    ++nodes;
    trace(0, cov, static_cast<int>(witness.size()));
    while (true) {
        if (complete(cov)) return true;
        int forced = -1, best_col = -1, best_count = 1000;
        for (int col = 0; col < NC; ++col) if (!covered(cov, col)) {
            int count = 0, last = -1;
            for (int r : col_rows[col]) if (compatible(r, cov)) { ++count; last = r; }
            if (count == 0) {
                ++dead_ends;
                trace(3, cov, col);
                return false;
            }
            if (count == 1) { forced = last; break; }
            if (count < best_count) { best_count = count; best_col = col; }
        }
        if (forced < 0) {
            vector<int> candidates;
            for (int r : col_rows[best_col]) if (compatible(r, cov)) candidates.push_back(r);
            sort(candidates.begin(), candidates.end());
            const size_t base = witness.size();
            for (int r : candidates) {
                Cols next = cov;
                add_row(r, next);
                witness.push_back(r);
                trace(2, cov, r);
                if (dfs(next, witness)) return true;
                witness.resize(base);
            }
            ++dead_ends;
            return false;
        }
        add_row(forced, cov);
        witness.push_back(forced);
        ++forced_steps;
        trace(1, cov, forced);
    }
}

int main(int argc, char** argv) {
    if (argc != 4) {
        cerr << "usage: residual_exact_cover instance.txt forbidden.txt trace.bin\n";
        return 2;
    }
    ifstream in(argv[1]);
    int nr, nc, ng, z;
    in >> nr >> nc >> ng;
    if (nr != NR || nc != NC) return 3;
    for (int r = 0; r < NR; ++r) for (int j = 0; j < 4; ++j) {
        in >> rows[r][j];
        col_rows[rows[r][j]].push_back(r);
    }
    for (int i = 0; i < ng * NR; ++i) in >> z;
    ifstream ff(argv[2]);
    int count, r;
    ff >> count;
    for (int i = 0; i < count; ++i) { ff >> r; forbidden[r] = 1; }
    trace_out.open(argv[3], ios::binary);
    Cols cov{};
    vector<int> witness;
    const auto begin = chrono::steady_clock::now();
    const bool found = dfs(cov, witness);
    const double seconds = chrono::duration<double>(chrono::steady_clock::now() - begin).count();
    trace_out.close();
    sort(witness.begin(), witness.end());
    cout << "{\"status\":\"PASS\",\"found\":" << (found ? "true" : "false")
         << ",\"nodes\":" << nodes
         << ",\"forced_steps\":" << forced_steps
         << ",\"dead_ends\":" << dead_ends
         << ",\"seconds\":" << seconds
         << ",\"witness\":[";
    for (size_t i = 0; i < witness.size(); ++i) { if (i) cout << ','; cout << witness[i]; }
    cout << "]}\n";
    return 0;
}
