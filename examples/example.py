from ehefluxes import fluxes
import matplotlib.pyplot as plt
import numpy as np

# myflux = fluxes.EHEFlux("cosmogenic_ahlers2010_1E185")
myflux = fluxes.EHEFlux("cosmogenic_ahlers2012")

energies = np.logspace(5, 12, 50)

flux_sum = myflux(energies, "sum")  # all flavor
flux_nuesum = myflux(energies, "nue_sum")  # just nue (2/6th of the all flavor)
flux_nue = myflux(energies, "nue")  # just nue (1/6th of the all flavor)

# we can also assign each event its own flavor
# by making an array of species, with an entry for each energy
# types = np.full(energies.shape, "nue", dtype=object)


fig, ax = plt.subplots(1, 1)
# plot GeV/cm^2/s/sr (for comparison sake)
ax.plot(energies, flux_sum*energies*energies, label="All-Species Sum")
ax.plot(energies, flux_nuesum*energies*energies, label="Nue+Nuebar Only")
ax.plot(energies, flux_nue*energies*energies, label="Nue Only")
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylabel(r'Flux [GeV/cm$^2$/s/sr]')
ax.set_xlabel(r'E$_{\nu}$ [GeV]')
ax.set_xlim([0.01, 1E12])
ax.set_ylim([1E-11, 1E-5])
ax.legend()
fig.tight_layout()
fig.savefig('flux_vs_e.png')
