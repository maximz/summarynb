# Jupyter Summary Notebooks

[![](https://img.shields.io/pypi/v/summarynb.svg)](https://pypi.python.org/pypi/summarynb)
[![CI](https://github.com/maximz/summarynb/actions/workflows/ci.yaml/badge.svg?branch=master)](https://github.com/maximz/summarynb/actions/workflows/ci.yaml)
[![](https://img.shields.io/badge/docs-here-blue.svg)](https://summarynb.maximz.com)
[![](https://img.shields.io/github/stars/maximz/summarynb?style=social)](https://github.com/maximz/summarynb)

## How do you show off your latest plots and tables when you meet with collaborators?

I used to drag my figures and tables into Powerpoint or a Google Doc. But it's tedious to import and position each item one-by-one. And it's even more painful to delete and re-import new versions after changing some code (are you positive you updated _all_ your figures to the latest version?)

Or you could scroll through your original Jupyter notebooks, live on screen share. Admit it, those notebooks are messy! Do you want to be switching tabs and scrolling through all your intermediate results during your meeting? What about the results you generated with scripts, not with notebooks? Most importantly, you can't look at two related figures side-by-side if they come from different sources.

## Present your results easily in a Jupyter "summary notebook".

A summary notebook is just a plain Jupyter notebook:

* A plain-English description of your analysis
* Shows important figures and tables inline with your text, imported by their filenames
* Committed and versioned with your code — meaning the summary notebook always reflects your analysis at that point in time, because it imports your latest result files.

**I write out the analysis as I go along, and incorporate relevant figures and tables inline**. Use `summarynb` to render any plot or table alongside your text, by its filename:
```python
from summarynb import show
show("plot.png")
```

  * _summarynb_ knows what to do for common file extensions

  * _summarynb_ uses sane defaults for figure sizes. You won't get ginormous figures like you'd see if showing an image with plain Markdown.


Sprucing up my summary notebooks with _summarynb_ means I can **look at related figures side-by-side**:

```python
from summarynb import show
show([ "plot1.png", "plot2.png", "results.csv" ])
```

  - For example, I'll review two visualizations of the same experiment, produced by different scripts and notebooks, in the same row of my summary notebook.

  - Or I'll pull in a results table alongside a figure. Let's say I run a simple linear regression. With a one-liner call to `show()`, I can review the scatterplot and a table of regression coefficients side-by-side.

  - Or if I have generated figures for every data point, I can review them all easily in an **auto-layout grid**. Just passing an array of entries to `chunks()` and then to `show()`, docs below.


Now I can cleanly **screen share results or send a Github link** to my collaborators. (Be concise. Only include the best figures and tables, not all the intermediate plots you generated.)

And I love that I can trust that the **presented results are up-to-date with the code** version I have checked out.

I **auto-regenerate my summary notebooks on every Git commit** by installing the optional git commit hook.

Plus I can **easily go back to the exact source.** I no longer have to wonder what generated a specific plot or table of interest, because I've got the filename right in front of me in the notebook. Just grep for that filename in your repo to track down which script or notebook wrote that file. (Or link to the source scripts/notebooks that generated your results!)

Since 2015, every project of mine has included a summary notebook, thanks to a tip from my former colleague Nick. This documentation practice **saves so much time when returning to old projects**.

## [Example summarynb usage.](https://nbviewer.jupyter.org/github/maximz/summarynb/blob/master/Example.ipynb)

## Your first `show()`

Install: `pip install summarynb`

Run this in a Jupyter notebook:

```python
from summarynb import show

show('myimage.png')
```

## Arrange in rows and columns

Here is a plot with an associated table, side-by-side:

```python
show(["run_1.png", "run_1.csv"])
```

Let's add a second row, as well as some headers:

```python
show(
    [
        ["run_1.png", "run_1.csv"],
        ["run_2.png", "run_2.csv"],
    ],
    headers=['Images', 'Tables']
)
```


## Customize the display

`show()` automatically decides how to display the given file path based on the file extension. You can customize this behavior.

Here are a couple examples:

```python
from summarynb import show, image, csv, indexed_csv

show(csv("run_summary.tsv", sep="\t", index_col=0))

show(
    [
        ["run_1.png", indexed_csv("run_1.csv")],
        [image("run_2.png"), indexed_csv("run_2.csv")],
    ],
    max_width=1200,
)
```

[See the docs for the full reference.](https://summarynb.maximz.com/summarynb.html)


## Auto Layout

Let's say you've generated 16 plots + tables. summarynb will automatically lay those out in rows and columns for you.

```python
from summarynb import show, image, indexed_csv, chunks

show(
    chunks(
        entries=[
            [
                image("run_%d.png" % (i + 1)),
                indexed_csv("run_%d.csv" % (i + 1)),
            ]
            for i in range(16)
        ],
        shape=4,
    )
)
```

## Automatically update on commit

Let's say you have a summary notebook named `summary.ipynb`. You can install a git pre-commit hook to run the notebook automatically when you make a commit:

```bash
# install the git hook
summarynb install

# mark for automatic execution on every commit
summarynb mark summary.ipynb
```

When you run `git commit`, summarynb will automatically re-execute `summary.ipynb` and add the changes to your commit. The notebooks marked for automatic execution are stored in `.summarynb.config`, which you can add to your Git repo to execute these notebooks in CI.

This automatic execution does not automatically add the modified summary notebook to your commit. Instead, it will pause your commit and allow you to review the updated notebook. Think of it as an automatic reminder to keep your summary notebooks up to date with the results you have on disk. Also, the hook strips metadata from the notebook, so that changes in execution timestamps don't count as "your summary notebook is out of date from what's in the git index".

Customize this hook further:

```bash
# view help
summarynb --help

# view list of auto-updated notebooks
summarynb list

# run manually
summarynb run

# unmark
summarynb unmark summary.ipynb

# uninstall the git hook
summarynb uninstall
```

You can alternatively install the hook within `.pre-commit-config.yaml` if you use [pre-commit](https://pre-commit.com):

```yaml
repos:
- repo: local
  hooks:
    - id: summarynb
      name: run summarynb
      entry: summarynb run
      language: system
      verbose: true
      always_run: true
      pass_filenames: false
```

## Other tips to make your notebooks beautiful

Adding a table of contents really makes summary notebooks shine. Here's how to install a Jupyter extension for this, and for code formatting. (Note: [requires nodejs](https://jupyterhub.readthedocs.io/en/stable/quickstart.html).)

```bash
# if using conda:
conda upgrade -c conda-forge -y jupyterlab nodejs

# code formatting and table of contents
pip install jupyterlab_code_formatter black
jupyter serverextension enable --py jupyterlab_code_formatter
jupyter labextension install -y --no-build @jupyterlab/toc @ryantam626/jupyterlab_code_formatter
jupyter labextension update -y --no-build --all # important that code formatter server and lab extension versions match
mkdir -p $HOME/.cache/black/19.10b0 # create directory for black grammar tables

# notebook diffing (nbdiff)
pip install nbdime
nbdime config-git --enable --global

# force a build to include code formatting, TOC, and nbdime-jupyterlab
jupyter lab build
```

May also need to set default formatter to black [following these instructions](https://jupyterlab-code-formatter.readthedocs.io/en/latest/how-to-use.html#changing-default-formatter). This involves adding the following in Jupyterlab Advanced Settings Editor:

```json
{
    "preferences": {
        "default_formatter": {
            "python": "black"
        }
    }
}
```

To update later:

```bash
# first update lab extension
jupyter labextension update --all
# then update server extension to matching version
pip install jupyterlab_code_formatter==x.x.x
```

## Development

```bash
pip install -r requirements_dev.txt
pip install -e .
make lint
make test

# bump version before submitting a PR against master (all master commits are deployed)
bump2version patch # possible: major / minor / patch

# also ensure CHANGELOG.md updated
```

TODOs:

* Accept pdf and other image formats
