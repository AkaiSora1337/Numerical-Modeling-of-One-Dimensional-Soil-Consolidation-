import numpy as np
import matplotlib.pyplot as plt

# Material parameters
h_cm, p_kN_per_m2, cv_cm2_per_day = 2.0, 200.0, 300.0

# Convert units
h = h_cm / 100.0  # cm to m
p = p_kN_per_m2 * 1000.0  # kN/m² to N/m²
cv = cv_cm2_per_day / (8.64e8)  # cm²/day to m²/s

# Numerical parameters
nz, nt = 21, 301
dt = 1.0  # seconds

# Calculate grid spacing and stability parameter (w)
z, dz = np.linspace(0, h, nz, retstep=True)
w = cv * dt / dz**2

# Check stability condition
if w > 0.5:
    print("Warning: Stability condition (w ≤ 0.5) not satisfied. Adjust dt or dz.")

# Initialize pressure array
u = np.empty((nz, nt))

# Set initial condition (n=0)
for i in range(nz):
    u[i, 0] = p

# Finite difference scheme (Single drainage: top impermeable, bottom drained)
for n in range(1, nt):
    # Apply BOTTOM boundary (drained, u=0)
    u[-1, n] = 0.0
    
    # Apply TOP boundary (impermeable: ∂u/∂z = 0 using ghost node method)
    u[0, n] = u[0, n-1] + 2 * w * (u[1, n-1] - u[0, n-1])
    
    # Update internal nodes
    for i in range(1, nz-1):
        u[i, n] = u[i, n-1] + w * (u[i-1, n-1] - 2*u[i, n-1] + u[i+1, n-1])

# Output results at specified time steps
output_array = u[:, ::60]  # Every 60th time step
np.savetxt("result_single_drained_ID.dat", output_array, fmt="%.4f")

print("Simulation completed. Results saved to result_single_drained_ID.dat")
# --- plot graph --- #
plt.figure()
plt.xlabel("Excess pore water pressure [N/m^2]")
plt.ylabel("Height [m]")
plt.plot(u[:,60],z,label="60s")
plt.plot(u[:,120],z,label="120s")
plt.plot(u[:,180],z,label="180s")
plt.plot(u[:,240],z,label="240s")
plt.plot(u[:,300],z,label="300s")
plt.legend()
plt.show()