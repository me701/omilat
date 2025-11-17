import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

# ----- load data -----
n, f_mv_row  = np.loadtxt("mv_row.out",  unpack=True)
n, f_mv_row_cc  = np.loadtxt("mv_row_cc.out",  unpack=True)
n, f_mv_col  = np.loadtxt("mv_col.out",  unpack=True)
n, f_mv_blas = np.loadtxt("mv_blas.out", unpack=True)
n, f_mv_blas_cc = np.loadtxt("mv_blas_cc.out", unpack=True)

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(n, f_mv_row,  label="row")
ax.plot(n, f_mv_row_cc,  label="row (C++)")
ax.plot(n, f_mv_col,  label="col")
ax.plot(n, f_mv_blas, label="libblas")
ax.plot(n, f_mv_blas_cc, label="libblas (C++)")

ax.set_xlabel("matrix size $n$")
ax.set_ylabel("GFLOP/s")
ax.grid(True, ls=":", alpha=0.5)
ax.set_ylim(0, 18)
ax.legend()

# conversions between n and matrix footprint
BYTES_PER_DOUBLE = 8

def n_to_mib(n):
    return BYTES_PER_DOUBLE * n * n / (1024.0**2)  # MiB for an n×n double matrix

def mib_to_n(mib):
    return np.sqrt(mib * (1024.0**2) / BYTES_PER_DOUBLE)

n_min, n_max = n.min(), n.max()
ax.set_xlim(n_min, n_max)

# secondary x-axis: matrix memory footprint in MiB 
secax = ax.secondary_xaxis('top', functions=(n_to_mib, mib_to_n))
secax.set_xlabel("matrix memory footprint (MiB)")

# which memory sizes to show?
desired_mib_marks = np.array([0.08, 1.25, 2, 4, 8, 16, 24, 32, 64, 128], dtype=float)

# keep only the ones that fall inside the *current* view
mib_lo, mib_hi = n_to_mib(ax.get_xlim()[0]), n_to_mib(ax.get_xlim()[1])
mib_ticks = desired_mib_marks[(desired_mib_marks >= mib_lo) & (desired_mib_marks <= mib_hi)]

# and set secondary ticks
secax.xaxis.set_major_locator(FixedLocator(mib_ticks))
secax.xaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{v:g}"))

plt.tight_layout()
plt.show()
