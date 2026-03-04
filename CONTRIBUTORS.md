# Contributors

**Repository:** `quantum-relaxation-ordering`  
**Programme:** Can Farther Beat Closer? — Quantum Relaxation Ordering in Trapped-Ion Systems  
**Affiliation:** Theory · Numerical · Experimental Quantum & Atomic Physics  
**Institution:** Albert-Ludwigs-Universität Freiburg

---

> **Canonical source:** `data/contributors.json` — the web page at `index.html` renders from this file. Edit the JSON to update all displays.

## Stewards

| Name | Track | Role | Contact |
|------|-------|------|---------|
| **Colla, Alessandra** | Theory | Steward · open quantum systems theory · spin-boson dynamics | alessandra.colla@physik.uni-freiburg.de |
| **Warring, Ulrich** | Experimental | Steward · trapped-ion platform · experimental design · pre-registration | ulrich.warring@physik.uni-freiburg.de |

---

## Contribution Tracks

This programme spans three functional tracks. If you are considering contributing, find the track that fits your expertise. You do not need to span all three — a single well-scoped contribution in one track is exactly what this open invitation is for.

### Theory Track

Focus: analytical and conceptual work on quantum relaxation ordering.

Possible contributions:
- Necessary and sufficient conditions for the non-Markovian quantum Mpemba effect
- Connection to Liouvillian exceptional points and non-Hermitian spectral structure
- Links to shortcuts to adiabaticity, dissipative state engineering
- Robustness analysis against decoherence channels not in the baseline model
- Extension to multi-qubit or multi-mode systems

Contact Colla, A. to discuss.

---

### Numerical Track

Focus: simulation pipeline, QuTiP toolbox, non-Markovian extensions.

Possible contributions:
- Module 03: Bloch sphere scan for Mpemba manifold (see `scripts/`)
- Module 04: HEOM implementation for non-Markovian bath
- Salvo's code integration for full spin-boson dynamics
- Platform-calibrated parameter runs (Ba⁺ / Ca⁺)
- Lamb-Dicke correction validation

See `scripts/README.md` for current pipeline status. Dependencies: Python ≥ 3.10, QuTiP ≥ 4.7.

Contact Warring, U. to discuss access to platform parameters.

---

### Experimental Track

Focus: trapped-ion realisation, tomography, pre-registered measurement protocol.

Possible contributions:
- Apparatus calibration for non-Markovian bath engineering
- State tomography protocol design for trace-distance measurement
- Pre-registration drafting and filing
- Experimental execution (contingent on pre-registration)

**Note on the 2016 dataset:** an archival dataset exists. It will be incorporated only after the analysis protocol is pre-registered. Experimental contributors are expected to agree to and participate in the pre-registration process. This is not a constraint — it is the scientific content of the collaboration.

Contact Warring, U.

---

## Acknowledgements

The following people have contributed to discussions that shaped this programme. They are not responsible for the current form of any document in this repository.

| Name | Affiliation | Contribution |
|------|-------------|--------------|
| Hasse, Florian | Experimental, Freiburg | Platform expertise · apparatus knowledge |
| Kemperman (aka Clos), Govinda | Experimental, Freiburg | 2016 dataset context · thesis work |
| Schätz, Tobias | Experimental, Freiburg | Spin-boson platform · discussion |
| Porras, Diego | Theory & Numerical | 2016 theory and numerical methods discussion |
| Michael *(surname TBC)* | Numerical | Numerical methods discussion |

---

## How to Contribute

1. Read the [Framework](framework.html) page first — especially the **Measure Box** and the **Pre-registration Commitment**.
2. Browse the [Numerics](numerics.html) toolbox and the `scripts/` notebooks.
3. Contact one of the stewards by email to discuss scope before opening a pull request.
4. All contributions are CC BY 4.0 (text) / MIT (code) unless explicitly agreed otherwise.

---

## Contribution Log

| Date | Contributor | Track | Description |
|------|------------|-------|-------------|
| 2026-03 | Warring, U. | All | Repository launch · solo open science |
| — | — | — | *open* |

---

*quantum-relaxation-ordering · v0.1-alpha · 2026*  
*Theory · Numerical · Experimental Quantum & Atomic Physics · Freiburg*
