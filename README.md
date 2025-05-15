# pynanigans
Python scripts for Oceananigans.jl NetCDF output

## Installation

### Using pip

You can install pynanigans directly from the repository:

```bash
pip install git+https://github.com/yourusername/pynanigans.git
```

Or install from a local clone:

```bash
git clone https://github.com/yourusername/pynanigans.git
cd pynanigans
pip install -e .
```

### Using conda

If you prefer using conda, you can create an environment with all dependencies:

```bash
# Clone the repository
git clone https://github.com/yourusername/pynanigans.git
cd pynanigans

# Create and activate conda environment
conda env create -f environment.yml
conda activate p39

# Install the package
pip install -e .
```

## Dependencies

The package requires:
- Python >= 3.9
- numpy
- xarray
- xgcm
- matplotlib

## Development

To set up a development environment:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pynanigans.git
cd pynanigans
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

3. Install development dependencies:
```bash
pip install pytest pytest-cov
```

4. Run tests:
```bash
pytest tests/
```

## License

See the [LICENSE](LICENSE) file for details.


