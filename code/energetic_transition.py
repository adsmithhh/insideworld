import numpy as np
import matplotlib.pyplot as plt

# CEST Two-Pool Steady-State: Energetic Transition Sim
# Purpose: Model magnetization transfer (A free <-> B bound) under RF saturation on B.
# Ties to CEST framework: State flips as prediction-error "ignition" analogs.
# Params: p_b=0.1 (bound frac), k_ex=20 s^-1 (exchange), R1_a=1 s^-1 (relax).

def lorentzian(offset, width=1.0):
    """Saturation efficiency on B: Lorentzian lineshape."""
    return 1 / (1 + (offset / width)**2)

# Core Params
p_b = 0.1
p_a = 1 - p_b
R1_a = 1.0
k_ex = 20.0  # Tweak here for tests (e.g., 50 for broader dip)
k_ab = k_ex * p_b / p_a  # Forward rate A->B
eff_transfer = k_ab / (R1_a + k_ab)  # Steady-state transfer eff

# Compute Z-Spectrum
offsets = np.linspace(-10, 10, 201)  # ppm
s_b = lorentzian(offsets)  # Sat eff on B
mz_a_norm = 1 - p_b * s_b * eff_transfer  # Normalized Mz_a

# Outputs
print("Sample Mz_a at offsets:")
for off in [-10, -5, 0, 5, 10]:
    idx = np.argmin(np.abs(offsets - off))
    print(f"{off:.1f} ppm: {mz_a_norm[idx]:.4f}")

max_dip = 1 - np.min(mz_a_norm)
print(f"\nMax dip: {max_dip:.4f} ({max_dip*100:.1f}% depletion) at {offsets[np.argmin(mz_a_norm)]:.1f} ppm")

# Plot (CEST Spectrum)
plt.figure(figsize=(8, 5))
plt.plot(offsets, mz_a_norm, 'b-', linewidth=2, label='Normalized Mz_a')
plt.axvline(0, color='r', linestyle='--', alpha=0.5, label='On-resonance (B)')
plt.xlabel('Saturation Offset (ppm)')
plt.ylabel('Normalized Mz_a')
plt.title('CEST Z-Spectrum: Energetic State Transition')
plt.ylim(0.92, 1.002)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('ce st_spectrum.png')  # Export for visuals/
plt.show()  # Or comment for non-GUI runs
