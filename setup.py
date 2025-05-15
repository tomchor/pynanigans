from setuptools import setup, find_packages

setup(
    name="pynanigans",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "xarray",
        "xgcm",
        "matplotlib",
    ],
    python_requires=">=3.9",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for working with Oceananigans data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pynanigans",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
) 