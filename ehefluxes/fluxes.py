from scipy import interpolate
import numpy as np
import importlib.resources as pkg_resources

from . import data

species = ['nue', 'nuebar', 'numu', 'numubar', 'nutau', 'nutaubar']


class EHEFlux:

    def __init__(self, flux_name):
        self.flux_name = flux_name
        self.load_and_spline_fluxes(self.flux_name)

    def load_and_spline_fluxes(self, flux_name):
        '''
        A function to load a flux table, and store splines of those
        fluxes in memory.

        Parameters
        ----------
        flux_name: string
            The name of the flux model whose flux table we should load.
            Flux tables should be stored in the `data` folder
            in the main `ehefluxes` package.

        Returns
        -------
        None
            This function has no return value, but is responsible
            for loading the flux table, and producing (and storing in memory),
            the splines to those fluxes.

        '''
        file = pkg_resources.open_text(data, f'{flux_name}.csv')
        file_content = np.genfromtxt(file, comments="#", delimiter=",",
                                     names=True, encoding='utf-16')
        self.make_flux_splines(file_content)
        
    def make_flux_splines(self, file_content):
        '''
        A function to interpolate the flux values
        with a 1D univariate spline.

        Parameters
        ----------
        file_content: numpy.ndarray
            A numpy ndarray containing the energies and flux values
            for a given extremely-high-energy diffuse flux.
            One column is the energies at which the fluxes are evaluated.
            Energies in GeV.
            Six additional columns, each for a species of neutrino
            (nue, nuebar, etc.).
            Fluxes in 1/GeV/cm/s/sr.

        Returns
        -------
        None
            This function has no return value, but is responsible
            for construction the class member `flux_splines`.
            This is a dictionary of scipy.UnivariateSpline.
            It maps the neutrino species to the spline for that flux.

        '''
        log10_e = np.log10(file_content['enu'])

        splines = {}
        for i, s in enumerate(species):
            log10_fluxes = file_content[s]
            splines[s] = interpolate.interp1d(
                log10_e, log10_fluxes,
                bounds_error=False,
                fill_value=-np.inf
            )
        self.flux_splines = splines
