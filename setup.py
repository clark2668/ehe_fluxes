from setuptools import setup

setup(
    name='ehefluxes',
    url='https://github.com/clark2688/ehefluxes',
    author='Brian Clark',
    author_email='baclark@msu.edu',
    packages=['ehefluxes'],
    install_requires=['numpy', 'scipy'],
    version='0.1',
    license='MIT',
    description='Package for returning EHE fluxes',
)
