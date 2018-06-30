#!/usr/bin/env python

from setuptools import setup

setup(name="trips-web",
        version='0.1',
        description='Command-line interface for the TRIPS web parser',
        author="Rik Bose",
        author_email="rbose@cs.rochester.edu",
        url="http://www.github.com/mrmechko/trips-web",
        scripts=['bin/trips-web'],
        install_requires=[
            'argparse'
        ],
        license="MIT"
   )

