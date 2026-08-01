#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#ifdef _OPENMP
#include <omp.h>
#endif
using U = std::uint64_t;
static U adjm[45], pm[45][45];
static int target;
static void dfs(int start, int depth, U selected, int edges, int triples,
                unsigned long long *hist, unsigned long long &count) {
  if (depth == target) {
    const int weight = 16 * target - 2 * edges + 4 * triples;
    ++hist[weight]; ++count; return;
  }
  const int need = target - depth;
  for (int v = start; v <= 45 - need; ++v) {
    const int de = std::popcount(adjm[v] & selected);
    int twice = 0; U x = selected;
    while (x) {
      const int a = std::countr_zero(x); x &= x - 1;
      twice += std::popcount(pm[v][a] & selected);
    }
    dfs(v + 1, depth + 1, selected | (U(1) << v), edges + de,
        triples + twice / 2, hist, count);
  }
}
int main(int argc, char **argv) {
  if (argc != 3) { std::cerr << "usage: worker K input.txt\n"; return 2; }
  target = std::stoi(argv[1]);
  if (target < 0 || target > 45) return 2;
  std::ifstream in(argv[2]); if (!in) return 2;
  for (auto &x : adjm) in >> x;
  for (auto &row : pm) for (auto &x : row) in >> x;
  std::vector<std::array<unsigned long long, 241>> h(45);
  std::vector<unsigned long long> counts(45);
#ifdef _OPENMP
#pragma omp parallel for schedule(dynamic,1)
#endif
  for (int first = 0; first <= 45 - target; ++first) {
    h[first].fill(0); counts[first] = 0;
    if (target == 0) { h[first][0] = 1; counts[first] = 1; continue; }
    dfs(first + 1, 1, U(1) << first, 0, 0, h[first].data(), counts[first]);
  }
  std::array<unsigned long long, 241> hist{}; unsigned long long total = 0;
  if (target == 0) { hist[0] = 1; total = 1; }
  else for (int first = 0; first < 45; ++first) {
    total += counts[first];
    for (int w = 0; w <= 240; ++w) hist[w] += h[first][w];
  }
  std::cerr << "count " << total << "\n";
  for (int w = 0; w <= 240; ++w) if (hist[w]) std::cout << w << ' ' << hist[w] << '\n';
}
