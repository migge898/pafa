# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()


setup(
    name="pafa",
    version="0.1.0",
    description="Python app for bachelor thesis at TH Bingen.",
    long_description=readme,
    author="Miguel Mioskowski",
    author_email="miguel.mioskowski@th-bingen.de",
    url="https://github.com/migge898/pafa",
    packages=find_packages(exclude=("tests", "docs")),
)