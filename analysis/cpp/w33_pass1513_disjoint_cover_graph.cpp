#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <vector>
using namespace std;
using Cover = array<uint64_t, 9>;

static bool disjoint(const Cover& a, const Cover& b) {
    for (int i = 0; i < 9; ++i) if (a[i] & b[i]) return false;
    return true;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        cerr << "usage: disjoint_cover_graph covers.bin\n";
        return 2;
    }
    ifstream in(argv[1], ios::binary);
    uint64_t n64 = 0;
    in.read(reinterpret_cast<char*>(&n64), sizeof(n64));
    if (!in || n64 > 1000000) return 3;
    const int n = static_cast<int>(n64);
    vector<Cover> covers(n);
    for (auto& c : covers) in.read(reinterpret_cast<char*>(c.data()), 9 * sizeof(uint64_t));
    if (!in) return 4;

    const int words = (n + 63) / 64;
    vector<vector<uint64_t>> adj(n, vector<uint64_t>(words));
    vector<int> degree(n, 0);
    uint64_t edges = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (!disjoint(covers[i], covers[j])) continue;
            adj[i][j >> 6] |= 1ULL << (j & 63);
            adj[j][i >> 6] |= 1ULL << (i & 63);
            ++degree[i]; ++degree[j]; ++edges;
        }
    }

    uint64_t triangles = 0;
    bool k4_exists = false;
    array<int, 3> first_triangle{-1, -1, -1};
    array<int, 4> first_k4{-1, -1, -1, -1};
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (((adj[i][j >> 6] >> (j & 63)) & 1ULL) == 0) continue;
            for (int w = 0; w < words; ++w) {
                uint64_t common = adj[i][w] & adj[j][w];
                if (w < (j >> 6)) common = 0;
                else if (w == (j >> 6)) {
                    const int bit = j & 63;
                    common &= bit == 63 ? 0 : ~((1ULL << (bit + 1)) - 1);
                }
                triangles += popcount(common);
                while (common) {
                    const int b = countr_zero(common);
                    common &= common - 1;
                    const int k = 64 * w + b;
                    if (first_triangle[0] < 0) first_triangle = {i, j, k};
                    if (k4_exists) continue;
                    for (int ww = 0; ww < words; ++ww) {
                        uint64_t fourth = adj[i][ww] & adj[j][ww] & adj[k][ww];
                        if (ww < (k >> 6)) fourth = 0;
                        else if (ww == (k >> 6)) {
                            const int bit2 = k & 63;
                            fourth &= bit2 == 63 ? 0 : ~((1ULL << (bit2 + 1)) - 1);
                        }
                        if (fourth) {
                            k4_exists = true;
                            first_k4 = {i, j, k, 64 * ww + countr_zero(fourth)};
                            break;
                        }
                    }
                }
            }
        }
    }

    int min_degree = numeric_limits<int>::max(), max_degree = 0, isolated = 0;
    for (int d : degree) {
        min_degree = min(min_degree, d);
        max_degree = max(max_degree, d);
        if (d == 0) ++isolated;
    }
    const int clique_number = triangles > 0 ? (k4_exists ? 4 : 3) : (edges > 0 ? 2 : 1);

    cout << "{\"status\":\"PASS\",\"vertices\":" << n
         << ",\"edges\":" << edges
         << ",\"triangles\":" << triangles
         << ",\"k4_exists\":" << (k4_exists ? "true" : "false")
         << ",\"clique_number\":" << clique_number
         << ",\"isolated_vertices\":" << isolated
         << ",\"min_degree\":" << min_degree
         << ",\"max_degree\":" << max_degree
         << ",\"first_triangle\":[" << first_triangle[0] << ',' << first_triangle[1] << ',' << first_triangle[2] << ']';
    if (k4_exists) {
        cout << ",\"first_k4\":[" << first_k4[0] << ',' << first_k4[1] << ',' << first_k4[2] << ',' << first_k4[3] << ']';
    }
    cout << "}\n";
    return 0;
}
