# Pass 12079: a context of clocks is the Hamming-code E8 on a pair of skew lines

Claude track. Builds on 12069, 12071 and 12080.

## Results

For each of the 81 choices of one clock per event of a context L:

1. **Frame and glue.** su(2)⁸ has 8 orthogonal frame roots, and its glue code is the extended Hamming code [8,4,4].
   E8 = 16 frame roots + 224 glue roots.
2. **Where the frame sits.** The frame roots lie on L ∪ L′, where L′ is disjoint from L. All 27 such lines occur, each
   for exactly 3 of the 81 choices.
3. **Codewords as events.**
   - 6 are unions of two matched pairs;
   - 4 + 4 are L or L′ with one event swapped for its partner.

   An AG(3,2) labelling makes the 14 codewords exactly the affine planes.
4. **Link to CP.** L ∪ L′ is the fixed set of a bosonic CP. 12080 shows that the CP's own clocks give this su(2)⁸.

## Prior art

E8 from the Hamming code is classical (Conway–Sloane ch. 8). New here: its realisation by clock involutions on W(3,3),
and the link to CP.

Producer: `analysis/w33_pass12079_a_context_of_clocks_is_a_hamming_code.py`.
