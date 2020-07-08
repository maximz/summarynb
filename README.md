# Jupyter Summary Notebooks

[![](https://img.shields.io/pypi/v/summarynb.svg)]([https://pypi.python.org/pypi/summarynb])
[![](https://img.shields.io/travis/maximz/summarynb.svg)](https://travis-ci.com/maximz/summarynb)

So you've just generated your latest plots and tables. How are you going to show your results off in your next meeting with your collaborators?

You could drag your figures into Powerpoint or a Google Doc. But it's tedious to import each figure and table one-by-one and position it manually. Even more painful when you change some code and need to delete and re-import your figures. And are you sure you updated all your figures? Are the versions all consistent?

Or you could scroll through your original notebooks, live on screen share. Admit it, those notebooks are messy. Do you want to be switching tabs and scrolling through all your intermediate results during your meeting? What about the results you generated with scripts, not with notebooks?

Enter _summarynb_.

**Present your results easily in Jupyter "summary notebooks":**

- **Versioned with your data.** Summary notebooks are versioned alongside your code and results, so you see exactly the figure and table versions you expect.
- **Beautiful.** Easily stack or arrange your figures and tables side-by-side, inline with your text. Sane defaults for figure sizes, so you don't get the ginormous figures you'd see if using standard Markdown to show an image.
- **Easy to use.**
    ```
    from summarynb import show
    show("plot.png")
    ```
    There, now you know how to use summarynb.
- **Shareable.** Just commit it to Git. Collaborators can view the rendered notebook on Github.
- **Updated automatically.** Optional git commit hook.

Since 2015, every project of mine has used summary notebooks, thanks to a tip from my former colleague Nick. I write out the analysis as I go along, and incorporate relevant figures and tables inline.

Not only has this made sharing results in group meetings much easier, but this documentation practice has saved me a ton of time when returning to old projects. And I love that I can trust that the presented results are up-to-date with the code version I have checked out. I encourage you to try it out with the instructions below.

## [Example.](https://nbviewer.jupyter.org/github/maximz/summarynb/blob/master/Example.ipynb)

## Best practices for summary notebooks

* Write out your analysis in plain English, so you can understand the logic when you return.
* Be concise. Only include the best figures and tables, not all the intermediate plots you generated.
* Link to the source scripts/notebooks that generated your results.
* Use a table of contents. (There are Jupyter extensions for this; see below.)

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

Note: [Requires nodejs](https://jupyterhub.readthedocs.io/en/stable/quickstart.html)

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
```

TODOs:

* Lint
* Pre-commit support
* Accept pdf and other image formats
