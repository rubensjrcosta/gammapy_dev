from astropy import units as u
import matplotlib.pyplot as plt
from gammapy.irf import EffectiveAreaTable2D

for instrument in ["HESS", "HESS2", "CTA"]:
    aeff = EffectiveAreaTable2D.from_parametrization(instrument=instrument)
    ax = aeff.plot_energy_dependence(label=instrument, offset=[0] * u.deg)

ax.set_yscale("log")
ax.set_xlim([1e-3, 1e3])
ax.set_ylim([1e3, 1e12])
plt.legend(loc="best")
plt.show()
