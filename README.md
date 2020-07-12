# Jupyter Summary Notebooks

[![](https://img.shields.io/pypi/v/summarynb.svg)](https://pypi.python.org/pypi/summarynb)
[![](https://img.shields.io/travis/maximz/summarynb.svg)](https://travis-ci.com/maximz/summarynb)
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

**Write out the analysis as you go along, and incorporate relevant figures and tables inline**.

Use `summarynb` to render any plot or table alongside your text, by its filename:
```python
from summarynb import show
show("plot.png")
```
    
  * _summarynb_ knows what to do for common file extensions
  
  * _summarynb_ uses sane defaults for figure sizes. You won't get ginormous figures like you'd see if showing an image with plain Markdown.
  

**Look at related figures side-by-side**:

```python
from summarynb import show
show([ "plot1.png", "plot2.png", "results.csv" ])
```

  - Review two visualizations of the same experiment, produced by different scripts and notebooks, in the same row of my summary notebook.

  - Pull in a results table alongside a figure. Imagine a linear regression: With a one-liner call to `show()`, review the scatterplot and a table of regression coefficients side-by-side.

  - If you've generated figures for every data point, review them all easily in an **auto-layout grid**. Just pass an array of entries to `chunks()` and then to `show()`, docs below.


**Screen share your summary notebook or send a Github link** to collaborators. Be concise. Only include the best figures and tables, not the intermediate plots.

**The presented results are up-to-date with the code** version checked out.

**Auto-regenerate your summary notebook on every Git commit** by installing the optional git commit hook. 

**Easily go back to the exact source.** What generated that plot or table? The filename is right in the notebook. Grep for that filename to track down which script or notebook wrote it. Or link in your summary notebook to the source scripts/notebooks that generated your results.

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

Let's say you have a summary notebook named `summary.ipynb`. You can install a git pre-commit hook to run the notebook automatically and incorporate it within your commit:

```bash
# install the git hook
summarynb install

# mark for automatic execution on every commit
summarynb mark summary.ipynb
```

When you run `git commit`, summarynb will automatically re-execute `summary.ipynb` and add the changes to your commit.

Customize this further:

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
make test

# bump version before submitting a PR against master (all master commits are deployed)
bump2version patch # possible: major / minor / patch

# also ensure CHANGELOG.md updated
```

TODOs:

* Lint
* Pre-commit support
* Accept pdf and other image formats
