#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#ifdef _OPENMP
#include <omp.h>
#else
static int omp_get_max_threads(){return 1;}
static int omp_get_thread_num(){return 0;}
static double omp_get_wtime(){return 0.0;}
#endif

using Row = std::array<std::uint64_t, 4>;
struct Orbit { std::uint32_t representative; std::uint32_t size; };

static int weight(const Row& row) {
    return std::popcount(row[0]) + std::popcount(row[1])
         + std::popcount(row[2]) + std::popcount(row[3]);
}

int main(int argc, char** argv) {
    if (argc < 4) {
        std::cerr << "usage: worker ROWS ORBITS OUTPUT [START STOP]\n";
        return 2;
    }
    std::array<Row, 45> rows{};
    std::ifstream row_input(argv[1]);
    for (auto& row : rows) {
        for (auto& limb : row) row_input >> std::hex >> limb;
    }
    if (!row_input) return 3;

    std::vector<Orbit> orbits;
    std::ifstream orbit_input(argv[2]);
    Orbit orbit{};
    while (orbit_input >> orbit.representative >> orbit.size) orbits.push_back(orbit);
    if (orbits.size() != 156) return 4;

    const int start = argc > 4 ? std::atoi(argv[4]) : 0;
    const int stop = argc > 5 ? std::atoi(argv[5]) : static_cast<int>(orbits.size());
    if (start < 0 || stop < start || stop > static_cast<int>(orbits.size())) return 5;

    constexpr int low_bits = 24;
    constexpr int high_bits = 6;
    constexpr std::uint64_t low_count = 1ULL << low_bits;
    constexpr int high_count = 1 << high_bits;

    const int threads = omp_get_max_threads();
    std::vector<std::array<unsigned long long, 241>> local(threads);
    std::array<unsigned long long, 241> global{};
    global.fill(0);
    const double beginning = omp_get_wtime();

    for (int index = start; index < stop; ++index) {
        for (auto& histogram : local) histogram.fill(0);
        Row residual{0, 0, 0, 0};
        const Orbit current = orbits[index];
        for (int bit = 0; bit < 15; ++bit) {
            if ((current.representative >> bit) & 1U) {
                for (int limb = 0; limb < 4; ++limb) residual[limb] ^= rows[30 + bit][limb];
            }
        }

        #pragma omp parallel for schedule(dynamic, 1)
        for (int high = 0; high < high_count; ++high) {
            const int thread = omp_get_thread_num();
            Row word = residual;
            for (int bit = 0; bit < high_bits; ++bit) {
                if ((high >> bit) & 1) {
                    for (int limb = 0; limb < 4; ++limb) word[limb] ^= rows[low_bits + bit][limb];
                }
            }
            local[thread][weight(word)]++;
            for (std::uint64_t gray_step = 1; gray_step < low_count; ++gray_step) {
                const int bit = std::countr_zero(gray_step);
                for (int limb = 0; limb < 4; ++limb) word[limb] ^= rows[bit][limb];
                local[thread][weight(word)]++;
            }
        }
        for (const auto& histogram : local) {
            for (int w = 0; w <= 240; ++w) global[w] += current.size * histogram[w];
        }
        if ((index - start + 1) % 10 == 0) {
            std::cerr << "completed " << (index - start + 1) << "/" << (stop - start)
                      << " orbits in " << (omp_get_wtime() - beginning) << " s\n";
        }
    }

    unsigned long long total = 0;
    for (const auto count : global) total += count;
    std::ofstream output(argv[3]);
    output << "# orbit_range " << start << " " << stop << "\n";
    output << "# weighted_words " << total << "\n";
    for (int w = 0; w <= 240; ++w) if (global[w]) output << w << " " << global[w] << "\n";
    std::cerr << "weighted_words=" << total << " elapsed=" << (omp_get_wtime() - beginning) << " s\n";
    return 0;
}
