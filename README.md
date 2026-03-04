# quantum-relaxation-ordering

**Can Farther Beat Closer? — Quantum Relaxation Ordering in Trapped-Ion Systems**

Open science repository · Solo launch · Contributions welcome

---

## Stewards

**Colla, Alessandra** · **Warring, Ulrich**  
Experimental Quantum & Atomic Physics  
Albert-Ludwigs-Universität Freiburg

---

## What This Is

This repository hosts a growing research programme aimed at testing the **non-Markovian quantum Mpemba effect** in a trapped-ion platform. It proceeds in public, ahead of collaboration, with an open numerics toolbox. Theory, numerics, tutorials, and eventually experimental data — all in one place, openly inspectable, freely usable.

The immediate experimental target is the prediction of **Strachan et al. (PRL 134, 220403, 2025)**: bath-memory-induced crossings in trace distance between spin reduced states and the reduced steady state (RSS).

## Site

Live at: [https://quantum-relaxation-ordering.github.io](https://quantum-relaxation-ordering.github.io)  
GitBook precursor: [Ions in Freiburg](https://uwarring.gitbook.io/ions-in-freiburg)

## Structure

```
index.html        ← Landing page / open invitation
dossier.html      ← Research dossier (classical → quantum)
framework.html    ← Falsifiable claim architecture
tutorial.html     ← Pedagogical tutorials (Lindblad, RSS, trace distance)
numerics.html     ← Simulation toolbox + live Chart.js results
references.html   ← Annotated reference landscape
style.css         ← Shared stylesheet
data/             ← JSON simulation outputs
scripts/          ← Python / QuTiP notebooks
```

## Numerics Toolbox

Python / QuTiP. Notebooks in `scripts/`.

```bash
pip install qutip numpy matplotlib scipy
jupyter notebook scripts/01_rss_finder.ipynb
```

## Pre-Registration Commitment

The analysis method will be pre-registered before any experimental data are examined. The 2016 archival dataset will be released here following that pre-registration.

## Licence

Text: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
Code: [MIT](https://opensource.org/licenses/MIT)

---

*Version 0.1-alpha · 2026*
