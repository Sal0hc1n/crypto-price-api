# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

from setuptools import setup

setup(
    name='crypto-price-api',
    version='0.1',
    author='The Internet',
    url='https://github.com/Sal0hc1n/crypto-price-api',
    description="API's for bitcoin exchanges",
    long_description='''Universal Cryptocurrency Exchanges' price API's''',
    license='MIT',
    packages=['exchanges'],
    install_requires=['python-dateutil==2.4.2', 'requests==2.9.1'],
    use_2to3=True
)
