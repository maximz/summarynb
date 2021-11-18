"""Console script for summarynb."""
import sys
import click
import os
import stat
import subprocess
import pandas as pd


@click.group()
def main(args=None):
    """Summary Notebooks Tool."""
    pass


def git_root_path():
    # when a hook is executed by git, it's executed in root of repo
    # when we run this as user, we need to manually go to $(git rev-parse --show-toplevel)
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    assert result.returncode == 0, "not a git repo!"
    return result.stdout.strip()


def path_to_config_file():
    return os.path.join(git_root_path(), ".summarynb.config")


def path_to_hook():
    githooks_dir = os.path.join(git_root_path(), ".git/hooks")
    assert os.path.isdir(githooks_dir), "not a git repo!"
    return os.path.join(githooks_dir, "pre-commit")


# TODO: write test that confirms these work identically from git root path as from subdir
# git_root_path()
# path_to_hook()
# path_to_config_file()


# maybe just make this a bash script that runs `summarynb run`?
hook_template = """#!/usr/bin/env python
import sys
from summarynb import cli
if __name__ == '__main__':
    sys.exit(cli.run())
"""


@main.command()
def install():
    fname = path_to_hook()
    # check whether there's already a hook
    if os.path.exists(fname):
        # ask for confirmation
        click.confirm(
            "This will overwrite existing pre-commit hook. Do you want to continue?",
            abort=True,
        )
    with open(fname, "w") as w:
        w.write(hook_template)
        # owner has all permissions including execute
        # group and others have read
        os.chmod(fname, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    print("installed")


@main.command()
def uninstall():
    fname = path_to_hook()
    # check whether there's already a hook
    if not os.path.exists(fname):
        print("no hook installed")
        sys.exit(1)
    if click.confirm("This will remove all pre-commit hooks. Do you want to continue?"):
        os.remove(fname)
        print("uninstalled")


def get_or_create_metadata():
    # retrieves or creates metadata file
    fname = path_to_config_file()
    if os.path.exists(fname):
        return pd.read_csv(fname).drop_duplicates()
    return pd.DataFrame(data=None, index=[], columns=["filename"], dtype="object")


def write_metadata(df):
    # writes metadata file
    df.drop_duplicates().to_csv(path_to_config_file(), index=None)


@main.command(name="list")
def list_nb():
    """reports which notebooks are registered for autorun, and whether they are found on disk"""
    df = get_or_create_metadata()
    df["exists"] = df["filename"].apply(os.path.exists)
    print(df)


def prune_nb():
    # TODO: prunes missing notebooks for autorun list
    pass


@main.command()
@click.argument("filepath")
def mark(filepath):
    """registers a notebook for autorun"""
    assert os.path.exists(filepath)
    df = get_or_create_metadata()
    assert not filepath in df["filename"].values, "Already registered"
    df = df.append(pd.DataFrame({"filename": filepath}, index=[-1]))
    write_metadata(df)
    print(
        "Registered notebook for autorun. Make sure git pre-commit hook is installed by running: summarynb install"
    )


@main.command()
@click.argument("filepath")
def unmark(filepath):
    """deregisters a notebook for autorun"""
    df = get_or_create_metadata().set_index("filename")
    # throws exception if filename not in index
    df = df.drop([filepath], axis=0).reset_index()
    write_metadata(df)


@main.command()
def run():
    """
    Execute notebooks in autorun list.

    Don't auto-add to git index - that's an anti-practice for git pre-commit hooks.
    When run locally, give the user a chance to review before committing. And CI should never be adding to the git index.

    Strip away metadata so that this isn't dependent on small changes in python/jupyter versions.
    Equivalent of:
        $ jupyter nbconvert --to notebook --execute Example.ipynb --inplace \
            --ClearMetadataPreprocessor.enabled=True \
                --ClearMetadataPreprocessor.clear_cell_metadata=True \
                    --ClearMetadataPreprocessor.clear_notebook_metadata=True \
                        --ClearMetadataPreprocessor.preserve_nb_metadata_mask='()';
    """
    df = get_or_create_metadata()
    print("Running summary notebooks. Skip this with --no-verify")
    for fname in df["filename"].values:
        print(fname)
        subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                fname,
                "--inplace",
                "--ClearMetadataPreprocessor.enabled=True",
                "--ClearMetadataPreprocessor.clear_cell_metadata=True",
                "--ClearMetadataPreprocessor.clear_notebook_metadata=True",
                "--ClearMetadataPreprocessor.preserve_nb_metadata_mask=()",
            ]
        )
        print()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
