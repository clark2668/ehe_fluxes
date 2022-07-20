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
        file = pkg_resources.open_text(data, f"{flux_name}.csv")
        file_content = np.genfromtxt(file, comments="#", delimiter=",",
                                     names=True, encoding="utf-16")
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
            Fluxes in 1/GeV/cm^2/s/sr.

        Returns
        -------
        None
            This function has no return value, but is responsible
            for construction the class member `flux_splines`.
            This is a dictionary of scipy.UnivariateSpline.
            It maps the neutrino species to the spline for that flux.

            Splining is done in log-space to make the splines more stable.
            (It is much easier to spline x and y values of order
            unity than 10E-9 GeV or 10E-20 1/GeV/cm^2/s/sr).

        '''
        log10_e = np.log10(file_content['enu'])

        splines = {}
        for i, s in enumerate(species):
            log10_fluxes = np.log10(file_content[s])
            splines[s] = interpolate.interp1d(
                log10_e, log10_fluxes,
                bounds_error=False,
                fill_value=-np.inf
            )
        self.flux_splines = splines

    def __call__(self, energies, which_species="sum"):
        '''
        A function to get flux values at a given energy.

        Do this by evaluating the splines (stored in memory) at these energies.

        Parameters
        ----------
        energies: list or numpy.ndarray
            A list or numpy.ndarray of energies at which
            the user would like to calculate the flux.
            Units of GeV.

        which_species: str or list or numpy.ndarray
            A keyword argument indicating which species of neutrino
            should be included at each energy bin.

            If which_species = "sum", the function will caculate
            the summed (not average!!) flux over all species.
            So total_flux = nue + nuebar + numu + numubar + nutau + nutaubar.

            If which_species = "SOMESPECIES", the function will calculate
            the flux for that species only.
            So if which_species = "nutau", then the function will only
            return the nutau component of the flux.
            E.g. total_flux = nutau.

            If which_species is a list or numpy.ndarray,
            the user can specify the species of neutrino *per energy bin*.
            So, which_species = ["nue", "numu", "nutau", ...]
            will calculate the nue component only for the first entry,
            the numu component only for the second entry, and so on.
            "sum" is not supported when using the function in array mode.

        Returns
        -------
        total_flux: numpy.ndarray
            An array containing the flux values at the energy bins.
            Units of 1/GeV/cm/s/sr.


        '''

        species_in_sum = []
        species_mask = {}

        # if necessary, convert energies to numpy array
        if isinstance(energies, list):
            energies = np.asarray(energies)

        # make holder array for final flux of same length as input energies
        total_flux = np.zeros(energies.shape)

        if isinstance(which_species, str):
            assert which_species in species or which_species == "sum", \
                f"Requested species {which_species} is not supported."

            mask = np.ones_like(energies)

            if which_species == "sum":
                # sum over all species
                for s in species:
                    species_in_sum.append(s)
                    species_mask[s] = mask
            else:
                # keep just the species the user requested
                species_in_sum.append(which_species)
                species_mask[which_species] = mask

        elif isinstance(which_species, list) \
                or isinstance(which_species, np.ndarray):

            assert len(energies) == len(which_species), \
                "Length of energy array does not match length of species array"

            if isinstance(which_species, list):
                # cast this as an array for our user
                which_species = np.asarray(which_species)

            for s in species:
                species_in_sum.append(s)
                mask = (which_species == s).astype(float)
                species_mask[s] = mask

        log_e_in = np.log10(energies)  # get energies in log10(E)

        # sum over all fluxes, applying mask where necessary
        for s in species_in_sum:

            # evaluate the spline
            this_spline = self.flux_splines[s](log_e_in)

            # convert the evaluated spline into a flux
            # by raising it to power 10
            this_flux = np.power(10., this_spline)

            # get the mask for this species
            mask = species_mask[s]

            # only add to the total where this flux is active
            total_flux += this_flux*mask

        return total_flux
