from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from setuptools import find_packages
from setuptools import setup

description = "Utilities for timing studies"

setup(
    name="trk_reco",
    version="0.0.1",
    description="Library for nothing",
    long_description=description,
    author="HEPTrkx",
    license="MIT License",
    keywords=['fun'],
    url="https://github.com/xju2/trk_reco",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7.13",
    ],
    scripts=[
        'scripts/parse_loginfo',
        'scripts/parse_perfmon',
    ],
)
