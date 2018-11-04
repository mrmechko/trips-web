#!/usr/bin/env python

from setuptools import setup

setup(name="trips-web",
        version='0.2.0',
        description='Command-line interface for the TRIPS web parser',
        author="Rik Bose",
        author_email="rbose@cs.rochester.edu",
        url="http://www.github.com/mrmechko/trips-web",
        entry_points = {
            "console_scripts": ['trips-web=tripsweb.query:main'],
        },
        install_requires=[
            'argparse',
            'xmltodict'
        ],
        license="MIT"
   )

