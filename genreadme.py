#!venv/bin/python3
""" updates README.md from the script's docstring """

import superscraper

with open('README.md', 'w') as fh:
    fh.write(superscraper.__doc__)

