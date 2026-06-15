# BT1119 — Direct paper-source patch chunks

BT1119 implements the paper-source patch path in small chunks rather than one monolithic helper.

## Added helpers

```text
tools/bt1119_patch_w33_sections.py
tools/bt1119_patch_holonet_sections.py
```

The W33 helper inserts staged W33 section includes before

```text
\section{The TOE Singularity Theorem}
```

The holonet helper inserts staged holonet section includes before

```text
\subsection{The ethos}
```

## Why this route

The connector repeatedly blocked full latest integrator patches and full-file direct replacement of the large TeX sources is unsafe.  These helper chunks are small, deterministic, idempotent, and avoid reconstructing the full source through the connector.

## Boundary

The helpers patch the main sources when run in a clone.  They are not themselves proof that the full papers compile.
