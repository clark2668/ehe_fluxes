from setuptools import setup

setup(
    name='ehefluxes',
    url='https://github.com/clark2688/ehefluxes',
    author='Brian Clark',
    author_email='baclark@msu.edu',
    packages=['ehefluxes'],
    package_data = {'ehefluxes': ['data/*']},
    include_package_data=True,
    python_requires='>= 3.7',
    install_requires=['numpy', 'scipy', 'matplotlib'],
    version='0.1',
    license='MIT',
    description='Package for returning EHE fluxes',
)
