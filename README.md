# Numerical Modeling of One-Dimensional Soil Consolidation

A course-based Python implementation of Terzaghi's one-dimensional consolidation equation using an explicit finite-difference method. The script simulates the dissipation of excess pore-water pressure in a homogeneous soil layer with **single drainage**, exports pressure profiles, and plots their evolution over time.

The project connects soil-mechanics boundary conditions with numerical implementation. It is an educational model, not a calibrated tool for geotechnical design.

## Model and numerical method

For a constant coefficient of consolidation, the governing equation is

$$
\frac{\partial u}{\partial t}
= c_v\frac{\partial^2 u}{\partial z^2},
$$

where $u$ is excess pore-water pressure, $c_v$ is the coefficient of consolidation, and $z$ is the coordinate through the soil layer.

The model uses a uniform initial pressure corresponding to an instantaneous load increment. The implemented boundary conditions are:

- **Impermeable top**, at $z=0$: $\partial u/\partial z=0$.
- **Drained bottom**, at $z=h$: $u=0$ during the time-stepping loop.

The initial array assigns the same pressure to every node, including the bottom node at $t=0$. The drained boundary is imposed from the first update onward.

Interior nodes are updated using forward Euler time integration and a central spatial difference:

$$
u_i^{n+1}=u_i^n+w\left(u_{i-1}^n-2u_i^n+u_{i+1}^n\right),
\qquad w=\frac{c_v\Delta t}{\Delta z^2}.
$$

The impermeable boundary is implemented with a reflected ghost node:

$$
u_0^{n+1}=u_0^n+2w\left(u_1^n-u_0^n\right).
$$

## Requirements

- Python 3
- NumPy
- Matplotlib

Install the packages with:

```bash
python -m pip install numpy matplotlib
```

## Run the simulation

Clone the repository and run the script:

```bash
git clone https://github.com/AkaiSora1337/Numerical-Modeling-of-One-Dimensional-Soil-Consolidation-.git soil-consolidation
cd soil-consolidation
python main.py
```

Use `python3` instead of `python` if that is how Python 3 is installed on your system. No external input data are required. The script writes its data file in the current working directory and opens a Matplotlib figure.

## Default parameters

Parameters are defined near the beginning of `main.py`; there is no command-line parameter interface.

| Parameter | Default | Meaning |
| --- | --- | --- |
| `h_cm` | `2.0` cm | Full soil-layer thickness |
| `p_kN_per_m2` | `200.0` kN/m² | Initial excess pore-water pressure |
| `cv_cm2_per_day` | `300.0` cm²/day | Coefficient of consolidation |
| `nz` | `21` | Number of spatial nodes, including boundaries |
| `nt` | `301` | Number of stored time levels, including the initial state |
| `dt` | `1.0` s | Time-step size |

The code converts these inputs to SI units before solving. With the defaults, the layer is `0.02 m` thick, the spatial step is `0.001 m`, and the simulation covers `0–300 s`.

### Stability

The explicit scheme requires

$$
w=\frac{c_v\Delta t}{\Delta z^2}\leq\frac{1}{2}.
$$

For the default parameters, $w\approx0.3472$, which satisfies this condition. The corresponding maximum time step is approximately `1.44 s` for the current spatial grid and material coefficient.

The script prints a warning if the condition is violated, but **does not stop execution**. Recheck stability whenever the time step, node count, layer thickness, or consolidation coefficient changes. A stable calculation does not, by itself, establish numerical accuracy.

## Outputs

### Pressure data

`result_single_drained_ID.dat` is a whitespace-delimited text file written with four decimal places. With the default settings, it contains **21 rows × 6 columns**:

- Rows correspond to spatial nodes from $z=0$ to $z=h$.
- Columns correspond to `0, 60, 120, 180, 240, 300 s`.
- Values are excess pore-water pressure in `N/m²` (Pa).

The file contains no headers or coordinate column. Reconstruct coordinates using `np.linspace(0, h, nz)`. Running the script again in the same directory overwrites the data file.

### Plot

The figure shows pressure profiles at `60, 120, 180, 240, and 300 s`. Pressure is on the horizontal axis and the spatial coordinate is on the vertical axis. Although the script labels the vertical axis `Height [m]`, its coordinate runs from the impermeable top at `z=0` to the drained bottom at `z=h`.

The script displays the figure with `plt.show()`; it does not automatically save an image file.

## Changing the example

Edit the material and numerical parameters directly in `main.py`. Note that:

- The final time is `(nt - 1) * dt`.
- Data export uses every 60th time level, so the physical output interval is `60 * dt` seconds.
- Plot indices and labels are hard-coded. If `dt` changes, update the labels; if `nt` is reduced below `301`, update the plotted indices as well.
- Thickness and material properties must use the input units shown in the parameter table.

## Scope and limitations

- The current repository implements **single drainage only**. A double-drainage variant is not included.
- The model assumes one-dimensional flow, a homogeneous layer, and a constant consolidation coefficient.
- It computes excess pore-water pressure, not settlement; stress-dependent properties, nonlinear behavior, and field calibration are outside its scope.
- Analytical benchmarking and systematic spatial/time-step convergence studies are not included in the repository.

Possible extensions include a double-drainage case, automatic enforcement of the stability condition, configurable output times, and comparison with an analytical solution.

## Author and context

**Wang Yanjun**, Kyoto University.

Developed as an undergraduate course-based exercise to study soil consolidation, drainage boundary conditions, and explicit finite-difference modeling.
