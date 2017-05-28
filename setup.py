# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

from setuptools import (
    setup,
    find_packages,
)

setup(
    name='bitcoin-price-api',
    version = '0.1',
    author='Anil Daoud',
    author_email='anil+github@via.ecp.fr',
    url='https://github.com/AnilDaoud/bitcoin-price-api',
    description="API's for cryptocurrencies exchanges",
    long_description='''Price API's for cryptycurrencies exchanges''',
    license='MIT',
    packages=['exchanges'],
    install_requires = ['requests', 'python-dateutil'],
    use_2to3 = True
)
