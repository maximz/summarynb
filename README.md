# Summary Notebooks

![https://pypi.python.org/pypi/summarynb](https://img.shields.io/pypi/v/summarynb.svg)

![https://travis-ci.com/maximz/summarynb](https://img.shields.io/travis/maximz/summarynb.svg)

![https://summarynb.readthedocs.io/en/latest/?badge=latest](https://readthedocs.org/projects/summarynb/badge/?version=latest)

Helpers to create summary Jupyter notebooks.

* Free software: MIT license
* Documentation: https://summarynb.readthedocs.io.


## Features

* TODO

Other tips to make your notebooks beautiful (requires nodejs):

```
# table of contents
jupyter labextension install @jupyterlab/toc

# code formatting
jupyter labextension install @ryantam626/jupyterlab_code_formatter
pip install jupyterlab_code_formatter black
jupyter serverextension enable --py jupyterlab_code_formatter

# build
jupyter lab build

# notebook diffing
pip install nbdime
nbdime config-git --enable --global
```

## Dev

```
pip install -r requirements_dev.txt
pip install -e .
```

## Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

* Cookiecutter: https://github.com/audreyr/cookiecutter
* `audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
