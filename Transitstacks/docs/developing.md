# Developing

## Setting up environment

### Installation
If you are going to be working on Transitstacks locally, you might want to clone it to your local machine and install it from the clone.  The -e will install it in [editable mode](https://pip.pypa.io/en/stable/reference/pip_install/?highlight=editable#editable-installs).


```bash
conda config --add channels conda-forge
conda create python=3.7 -n <my_conda_environment>
conda activate <my_lasso_environment>
git clone https://github.com/e-lo/Transitstacks
cd Transitstacks
pip install -e .
pip install -r dev-requirements.txt
```

Notes:

1. The -e installs it in editable mode.
2. If you are not part of the project team and want to contribute code bxack to the project, please fork before you clone and then add the original repository to your upstream origin list per [these directions on github](https://help.github.com/en/articles/fork-a-repo).
3. if you wanted to install from a specific tag/version number or branch, replace `@main` with `@<branchname>`  or `@tag`
4. If you want to make use of frequent developer updates for network wrangler as well, you can also install it from clone by copying the instructions for cloning and installing Lasso for Network Wrangler

### Other tools
If you are going to be doing development, we also recommend a few other tools:
 -  a good IDE such as [VS Code](https://code.visualstudio.com/), Sublime Text, etc.
 with Python syntax highlighting turned on.
 - [GitHub Desktop](https://desktop.github.com/) to locally update your clones

## Development Workflow

General steps: 
1. Fork it (https://github.com/e-lo/Transitstacks/fork)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Add your feature, add tests which test your feature, document your feature, and pass all tests.
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request

## Tests
Tests are written for `pytest` and can be run using the command `pytest`.

Tests are run with the [pyTest](pytest.org)/

### Test structure

- Tests marked with `@pytest.mark.skipci` will not run by the continuous integration tests

### Setup

Pytest can be installed using one of the following options.

Install along with all development requirements (recommended):
```sh
pip install -r dev-requirements.txt
```
Install using PIP: 
```sh
pip install pytest
```
Install using Conda: 
```sh
conda install pytest
```

### Running tests

1. Run all tests
```sh
pytest 
```

2. Run tests in `test_basic.py`
```sh
pytest tests/test_basic.py
```

3. Run tests decorated with @pytest.mark.favorites decorator
```sh
pytest -m favorites
```

4. Run all tests and print out stdout
```sh
pytest -s
```

5. Run all tests which are run on the CI server
```sh
pytest -v -m "not skipci"
```

## Documentation
Docstrings are written in [google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) and auto-rendered as api documentation using [mkdocstrings](https://mkdocstrings.github.io/) as specified in `/docs/api.md`. 

Documentation uses [mkdocs](https://www.mkdocs.org/) and is in the `/docs` folder.  It can be rendered locally using the command `mkdocs serve`. 


**Reminder**
This code is offered with the [AGPL 3.0](LICENSE) license and developed on behalf of the [California Integrated Travel Project](http://calitp.org), which is **share-alike**. 