# Starting Out

## Installation

If you are managing multiple python versions, we suggest using [`virtualenv`](https://virtualenv.pypa.io/en/latest/) or [`conda`](https://conda.io/en/latest/) virtual environments.

The following instructions create and activate a conda environment (recommended) in which you can install:

```bash
conda config --add channels conda-forge
conda create python=3.7 -n <my_conda_environment>
conda activate <my_conda_environment>
```

Basic installation instructions are as follows:

```bash
pip install git+https://github.com/e-lo/Transitstacks@main
```

#### Bleeding Edge
If you want to install a more up-to-date or development version, you can do so by installing it from the `develop` branch as follows:

```bash
conda config --add channels conda-forge
conda create python=3.7  -n <my_conda_environment>
conda activate <my_conda_environment>
pip install git+https://github.com/e-lo/Transitstacks@develop
```