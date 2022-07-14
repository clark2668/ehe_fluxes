from setuptools import setup

setup(
    name='ehe_fluxes',
    url='https://github.com/clark2688/ehe_fluxes',
    author='Brian Clark',
    author_email='baclark@msu.edu',
    packages=['ehe_fluxes'],
    install_requires=['numpy', 'scipy'],
    version='0.1',
    license='MIT',
    description='Package for returning EHE fluxes',
)