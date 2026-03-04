# Scripts / Notebooks

Python / QuTiP simulation pipeline for the quantum-relaxation-ordering programme.

## Notebooks

| File | Status | Description |
|------|--------|-------------|
| `01_rss_finder.ipynb` | active | Reduced steady state finder. Parameter scans. |
| `02_rss_diagnostic.ipynb` | active | RSS diagnostic check. Lamb-Dicke comparison. |
| `03_mpemba_scan.ipynb` | in progress | Bloch sphere scan for Mpemba manifold. |
| `04_nonmarkov.ipynb` | planned | HEOM for non-Markovian bath. Crossing time scaling. |

## Installation

```bash
pip install qutip numpy matplotlib scipy jupyter
```

## Output

Notebooks export results to `../data/` as JSON for rendering on the website.

## Dependencies

- Python ≥ 3.10
- QuTiP ≥ 4.7
- numpy, matplotlib, scipy, jupyter
