# ehefluxes
A small package for providing ehe fluxes

ehefluxes is a lightweight python3-based package for calculating EHE/UHE ("extremely high energy"/"ultra high energy" ) diffuse neutrino fluxes.
"Extremely/ultra" high generally means >10 PeV.
Because the fluxes are diffuse, only energy dependence is supported
(no zenith dependence).

## Installation

Installation of ehefluxes is easy with pip:

    git clone https://github.com/clark2668/ehefluxes.git
    cd ehefluxes
    pip install . 

If you plan on actively contributing or developing, then installing with
symlink is useful:

    pip install -e .

A user may also find it helpul to install into user space, or into a 
specific target directory:

    pip install --user .
    pip install . --target=/path/to/my/install

If doing the latter, remember to update your PYTHONPATH.


### Prerequisites

`ehefluxes` is dependency light, requiring numpy, scipy, and matplotlib.
Python >=3.7 (for manging fluxes through importlib).

## Fluxes & Units

Manging units in neutrino flux measurements is always challenging.
In this package, the base unit of energy is GeV.
The code returns fluxes in *particle flux*, meaning 1/cm2/s/sr.
This is often most convenient for weighting Monte Carlo generated events.
This corresponds to the EF, or "energy times flux normalization".
A user can generate the E^2F, or "e-squared normalization" by multiplying
by a copy of energy. 

Internally, the code stores and splines fluxes in units of 1/GeV/cm2/s/sr.

### Adding your Own Fluxes

Adding new fluxes can be done by adding the relevant csv file to the 
`ehefluxes/data` folder.
The file should contain seven columns.
The first column should specify the neutrino energy in GeV.
The next six columns should give the per-species neutrino fluxes
in units of 1/GeV/cm2/s/sr (see units discussion above).

The first line should specify the column headers, all lower case. E.g.

    enu, nue, nuebar, numu, numubar, nutau, nutaubar

The order of the flux columns does not matter.
(E.g. nue, nuebar, etc. can be listed in any order.)
Comments may be added to the file at any point by prepending the
line with a pound sign, e.g.

    enu, nue, nuebar, numu, numubar, nutau, nutaubar
    # we can comment here that this flux is an ahlers fluxs
    # in units of GeV, and 1/GeV/cm2/s/sr
    1e9, 3e-24, ....

Having separate columns for each species supports fluxes which are 
not equipartition between flavors and particles/antiparticles.
If the flux of interest *is* equipartition (equal distribution 
between flavors and nu/nubar) the user must still provide six columns.
In such a case, the user would divide the total flux by 1/6th,
and use those identical values in each column.
