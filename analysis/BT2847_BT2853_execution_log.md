# Passes 2847--2853 execution log

Local exact execution on 3 August 2026:

```text
RUN 2847
DONE 2847
RUN 2848
DONE 2848
RUN 2849
DONE 2849
RUN 2850
DONE 2850
RUN 2851
DONE 2851
RUN 2852
DONE 2852
PASS 8/8
28 fixed taps; 24 resampled affine-square bits; Aut orders 32 and 6912;
noisy-M36 golden threshold; adaptive horizon 4.
```

Focused frozen-certificate/RTL-contract regressions:

```text
......                                                                   [100%]
6 passed in 0.09s
```

The exact verifier recomputation took approximately 31 seconds and 203 MB resident memory in the local Python environment. Icarus, Yosys, nextpnr, and Tectonic evidence is intentionally delegated to the observable GitHub Actions workflow; no local hardware figures are inferred.
