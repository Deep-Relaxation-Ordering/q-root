"""
run_simulations.py
==================
Quantum Relaxation Ordering — Module 01 simulation runner
Stewards: Colla, A. & Warring, U.
Affiliation: Theory · Numerical · Experimental Quantum & Atomic Physics, Freiburg

Runs in QuTiP 5.x. Exports results to ../data/rss_dynamics.json.

Usage:
    python3 run_simulations.py

Status: ILLUSTRATIVE — parameters chosen for conceptual clarity, not
platform calibration. Pre-registration pending. Not experimental data.
"""

import numpy as np
import json
import os
from datetime import datetime, timezone
import qutip as qt

print(f"QuTiP {qt.__version__} | NumPy {np.__version__}")
print(f"Run: {datetime.now(timezone.utc).isoformat()}")
print("=" * 60)

# ── Parameters ────────────────────────────────────────────────────────────────
OMEGA0  = 1.0    # spin transition frequency  [ω₀ = 1, sets timescale]
OMEGAM  = 1.0    # motional mode frequency
G       = 0.05   # spin-motion coupling  (Lamb-Dicke: g ≪ ωm)
GAMMA   = 0.02   # Markovian bath decay rate
N_BAR   = 5.0    # mean phonon number of bath
N_FOCK  = 20     # Fock space truncation
T_END   = 200.0  # simulation end time
N_STEPS = 80     # time points

ETA_VALUES = [0.0, 0.05, 0.10, 0.15, 0.20]   # Lamb-Dicke scan


# ── Operators ─────────────────────────────────────────────────────────────────
def build_system(omega0=OMEGA0, omegam=OMEGAM, g=G, gamma=GAMMA,
                 n_bar=N_BAR, N=N_FOCK, eta=0.0):
    """
    Build Hamiltonian and jump operators for spin + motional mode + Markovian bath.

    H = (ω₀/2)σ_z + ωm a†a + g(σ₊ + σ₋)(a + a†)  [Lamb-Dicke]
    or with first η² correction when eta > 0.

    Jump operators: motional mode ↔ thermal bath at n_bar.
    """
    sm  = qt.tensor(qt.sigmam(), qt.qeye(N))
    sp  = qt.tensor(qt.sigmap(), qt.qeye(N))
    sz  = qt.tensor(qt.sigmaz(), qt.qeye(N))
    a   = qt.tensor(qt.qeye(2),  qt.destroy(N))
    ada = a.dag() * a

    # Coupling operator
    x = a + a.dag()
    if eta > 0.0:
        # First Lamb-Dicke correction: expand e^{iη(a+a†)} to order η²
        x_coup = x - (eta**2 / 2.0) * (x * x)
    else:
        x_coup = x

    H = (omega0 / 2.0) * sz + omegam * ada + g * (sp + sm) * x_coup

    c_ops = [
        np.sqrt(gamma * (n_bar + 1.0)) * a,       # phonon decay
        np.sqrt(gamma * n_bar)         * a.dag(),  # phonon creation
    ]
    return H, c_ops, dict(sm=sm, sp=sp, sz=sz, a=a, ada=ada)


def trace_distance(rho, sigma):
    """D(ρ,σ) = ½ Tr|ρ−σ|"""
    diff   = rho - sigma
    evals  = diff.eigenenergies()
    return float(0.5 * np.sum(np.abs(evals)))


# ── 1. Reduced Steady State ───────────────────────────────────────────────────
print("\n[1] Computing reduced steady state...")
H, c_ops, ops = build_system()

rho_ss_total = qt.steadystate(H, c_ops)
rho_ss_spin  = rho_ss_total.ptrace(0)

bx = float(qt.expect(qt.tensor(qt.sigmax(), qt.qeye(N_FOCK)), rho_ss_total))
by = float(qt.expect(qt.tensor(qt.sigmay(), qt.qeye(N_FOCK)), rho_ss_total))
bz = float(qt.expect(qt.tensor(qt.sigmaz(), qt.qeye(N_FOCK)), rho_ss_total))
purity = float((rho_ss_spin * rho_ss_spin).tr().real)

print(f"  RSS Bloch vector : [{bx:.4f}, {by:.4f}, {bz:.4f}]")
print(f"  RSS purity       : {purity:.4f}")


# ── 2. Liouvillian Spectrum ───────────────────────────────────────────────────
print("\n[2] Computing Liouvillian spectrum...")
L      = qt.liouvillian(H, c_ops)
# QuTiP 5: eigenstates via superoperator — use lindblad_dissipator approach
# Flatten to matrix, take eigenvalues
L_mat  = L.full()
evals_all = np.linalg.eigvals(L_mat)
# Sort by |Re(λ)| ascending — slowest modes first
evals_sorted = sorted(evals_all, key=lambda x: abs(x.real))
evals_top = evals_sorted[:6]

print(f"  {'k':>2}  {'Re(λ)':>12}  {'Im(λ)':>12}  {'τ_k':>12}")
liouv_data = []
for k, ev in enumerate(evals_top):
    re, im = float(ev.real), float(ev.imag)
    tau = float(-1.0/re) if re < -1e-10 else None
    tau_str = f"{tau:.3f}" if tau else "∞"
    print(f"  {k:>2}  {re:>12.6f}  {im:>12.6f}  {tau_str:>12}")
    liouv_data.append({"k": k, "Re_lambda": re, "Im_lambda": im,
                        "tau": tau})

relax_gap = abs(evals_top[1].real)
relax_tau = float(1.0 / relax_gap)
print(f"\n  Relaxation gap Δ = {relax_gap:.6f}")
print(f"  Dominant τ_relax  = {relax_tau:.3f}  [units: 1/ω₀]")


# ── 3. RSS Diagnostic Check ───────────────────────────────────────────────────
print("\n[3] RSS diagnostic check...")
rho_motion_thermal = qt.thermal_dm(N_FOCK, N_BAR)
rho0_diag = qt.tensor(rho_ss_spin, rho_motion_thermal)

times = np.linspace(0, T_END, N_STEPS)
result_diag = qt.mesolve(H, rho0_diag, times, c_ops, [])

D_diag = np.array([
    trace_distance(state.ptrace(0), rho_ss_spin)
    for state in result_diag.states
])

peak_idx = int(np.argmax(D_diag))
print(f"  Peak D  = {D_diag[peak_idx]:.5f}  at t = {times[peak_idx]:.1f}")
print(f"  Final D = {D_diag[-1]:.6f}  (target → 0)")
assert D_diag[-1] < 0.01, "RSS diagnostic failed: system did not return to steady state"
print("  ✓ RSS diagnostic passed")


# ── 4. Mpemba State Pair ──────────────────────────────────────────────────────
print("\n[4] Mpemba scenario — state pair search...")

# State A: excited spin |↑⟩⟨↑| — maximally far along σ_z axis
rho_A_spin = qt.ket2dm(qt.basis(2, 0))

# State B: mixture — scan α to find D_B < D_A and observe crossing
# Mix RSS with excited state: ρ_B = α·ρ_ss + (1-α)|↑⟩⟨↑|
best_crossing = None
best_alpha    = None

for alpha in np.linspace(0.3, 0.7, 9):
    rho_B_try = alpha * rho_ss_spin + (1 - alpha) * qt.ket2dm(qt.basis(2, 0))
    rho_B_try = rho_B_try / rho_B_try.tr()
    D0_A = trace_distance(rho_A_spin, rho_ss_spin)
    D0_B = trace_distance(rho_B_try, rho_ss_spin)
    if D0_B >= D0_A:
        continue   # B must start closer

    rho0_A = qt.tensor(rho_A_spin,  rho_motion_thermal)
    rho0_B = qt.tensor(rho_B_try, rho_motion_thermal)
    res_A  = qt.mesolve(H, rho0_A, times, c_ops, [])
    res_B  = qt.mesolve(H, rho0_B, times, c_ops, [])
    D_A_try = np.array([trace_distance(s.ptrace(0), rho_ss_spin) for s in res_A.states])
    D_B_try = np.array([trace_distance(s.ptrace(0), rho_ss_spin) for s in res_B.states])

    cross = np.where(D_A_try < D_B_try)[0]
    if len(cross) > 0:
        t_cross = float(times[cross[0]])
        print(f"  α={alpha:.2f}  D0_A={D0_A:.4f}  D0_B={D0_B:.4f}  t*={t_cross:.2f}  ✓")
        if best_crossing is None or t_cross < best_crossing:
            best_crossing = t_cross
            best_alpha    = alpha
            D_A_best      = D_A_try
            D_B_best      = D_B_try
            D0_A_best     = D0_A
            D0_B_best     = D0_B
            rho_B_best    = rho_B_try
    else:
        print(f"  α={alpha:.2f}  D0_A={D0_A:.4f}  D0_B={D0_B:.4f}  no crossing")

if best_crossing:
    print(f"\n  Best pair: α={best_alpha:.2f}, t*={best_crossing:.2f}")
else:
    print("\n  ✗ No crossing found — widening search or adjusting parameters needed")
    # Fallback: store trajectories anyway
    rho0_A = qt.tensor(rho_A_spin, rho_motion_thermal)
    res_A  = qt.mesolve(H, rho0_A, times, c_ops, [])
    D_A_best = np.array([trace_distance(s.ptrace(0), rho_ss_spin) for s in res_A.states])
    D_B_best = D_diag  # fallback
    D0_A_best = trace_distance(rho_A_spin, rho_ss_spin)
    D0_B_best = D_diag[0]
    rho_B_best = rho_ss_spin


# ── 5. Lamb-Dicke Correction Scan ────────────────────────────────────────────
print("\n[5] Lamb-Dicke correction scan...")
ld_scan_results = []

for eta in ETA_VALUES:
    print(f"  η = {eta:.2f}", end="  ", flush=True)
    H_i, c_ops_i, _ = build_system(eta=eta)
    rho_ss_i  = qt.steadystate(H_i, c_ops_i)
    rho_ss_spin_i = rho_ss_i.ptrace(0)

    D0_A_i = trace_distance(rho_A_spin, rho_ss_spin_i)
    D0_B_i = trace_distance(rho_B_best, rho_ss_spin_i)

    rho0_A_i = qt.tensor(rho_A_spin,  rho_motion_thermal)
    rho0_B_i = qt.tensor(rho_B_best, rho_motion_thermal)

    res_A_i = qt.mesolve(H_i, rho0_A_i, times, c_ops_i, [])
    res_B_i = qt.mesolve(H_i, rho0_B_i, times, c_ops_i, [])

    D_A_i = np.array([trace_distance(s.ptrace(0), rho_ss_spin_i) for s in res_A_i.states])
    D_B_i = np.array([trace_distance(s.ptrace(0), rho_ss_spin_i) for s in res_B_i.states])

    cross_i = np.where(D_A_i < D_B_i)[0]
    t_cross_i = float(times[cross_i[0]]) if len(cross_i) > 0 else None

    result_i = {
        "eta": eta,
        "D0_A": round(float(D0_A_i), 5),
        "D0_B": round(float(D0_B_i), 5),
        "crossing_time": round(t_cross_i, 3) if t_cross_i else None,
        "D_A": [round(float(v), 6) for v in D_A_i],
        "D_B": [round(float(v), 6) for v in D_B_i],
    }
    ld_scan_results.append(result_i)

    cross_str = f"t*={t_cross_i:.2f}" if t_cross_i else "no crossing"
    print(f"D0_A={D0_A_i:.4f}  D0_B={D0_B_i:.4f}  {cross_str}")


# ── 6. Export JSON ────────────────────────────────────────────────────────────
print("\n[6] Exporting to data/rss_dynamics.json...")

output = {
    "meta": {
        "description": "Module 01 — RSS finder, diagnostic, Mpemba scenario, LD scan",
        "status": "COMPUTED — illustrative parameters, not platform-calibrated. Pre-registration pending.",
        "system": "spin-1/2 + single motional mode + Markovian bath",
        "parameters": {
            "omega0": OMEGA0,
            "omegam": OMEGAM,
            "g": G,
            "gamma": GAMMA,
            "n_bar": N_BAR,
            "N_fock": N_FOCK,
            "t_end": T_END,
            "n_steps": N_STEPS,
        },
        "units": "dimensionless (ω₀ = 1)",
        "generated": datetime.now(timezone.utc).isoformat(),
        "tool": f"QuTiP {qt.__version__} · NumPy {np.__version__}",
        "runner": "scripts/run_simulations.py",
    },
    "steady_state": {
        "bloch_vector": [round(bx, 6), round(by, 6), round(bz, 6)],
        "purity": round(purity, 6),
    },
    "liouvillian_spectrum": {
        "relaxation_gap": round(relax_gap, 8),
        "dominant_tau": round(relax_tau, 4),
        "eigenvalues": liouv_data,
    },
    "rss_check": {
        "description": "Spin initialised in RSS. Motion thermal at n_bar. D(ρ_spin(t), ρ_ss) rises then returns.",
        "times": [round(float(t), 3) for t in times],
        "D_rss_init": [round(float(d), 6) for d in D_diag],
        "peak_D": round(float(D_diag[peak_idx]), 5),
        "peak_time": round(float(times[peak_idx]), 2),
        "final_D": round(float(D_diag[-1]), 7),
    },
    "mpemba_scenario": {
        "description": "State A (farther) vs State B (closer). Mpemba effect: A crosses below B.",
        "alpha_B": best_alpha,
        "D0_A": round(float(D0_A_best), 5),
        "D0_B": round(float(D0_B_best), 5),
        "crossing_time_computed": round(float(best_crossing), 3) if best_crossing else None,
        "times": [round(float(t), 3) for t in times],
        "D_state_A": [round(float(v), 6) for v in D_A_best],
        "D_state_B": [round(float(v), 6) for v in D_B_best],
    },
    "ld_scan": {
        "description": "Lamb-Dicke correction scan. Same state pair, varying η.",
        "eta_values": ETA_VALUES,
        "results": ld_scan_results,
    },
}

out_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'data', 'rss_dynamics.json'
)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w') as f:
    json.dump(output, f, indent=2)

size_kb = os.path.getsize(out_path) / 1024
print(f"  Written: {os.path.abspath(out_path)}")
print(f"  Size   : {size_kb:.1f} kB")
print("\n✓ All simulations complete.")
