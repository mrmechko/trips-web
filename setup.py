#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="trips-web",
        version='1.0.11',
        description='Command-line interface for the TRIPS web parser',
        author="Rik Bose",
        author_email="rbose@cs.rochester.edu",
        url="http://www.github.com/mrmechko/trips-web",
        packages=find_packages(),
        entry_points = {
            "console_scripts": ['trips-web=tripsweb.query:main', 'make-input-terms=tripsweb.inputterms:main'],
        },
        install_requires=[
            'argparse',
            'xmltodict'
        ],
        license="MIT",
        python_requires=">3.0"
   )

