from setuptools import setup, find_packages
import tomli

# Read version from pyproject.toml
with open("pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)
    version = pyproject["project"]["version"]

setup(
    name="pynanigans",
    version=version,
    packages=find_packages(),
    install_requires=[
        "numpy",
        "xarray",
        "xgcm",
        "matplotlib",
    ],
    python_requires=">=3.9",
    author="Tomas Chor",
    author_email="contact@tomaschor.xyz",
    description="A Python package for working with Oceananigans data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pynanigans",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
)
