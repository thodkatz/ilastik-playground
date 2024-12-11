from io import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

setup(
    name="ilastik-playground",
    version="0.0.1",
    description="",
    packages=find_packages(exclude=["tests"]),
    install_requires=[

    ],
    extras_require={},
)
