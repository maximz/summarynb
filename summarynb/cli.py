"""Console script for summarynb."""
import sys
import click
import os
import stat
import subprocess


@click.group()
def main(args=None):
    """Console script for summarynb."""
    # header for every command
    click.echo("==Summary Notebooks Tool==")
    return 0

def git_root_path():
    # when a hook is executed by git, it's executed in root of repo
    # when we run this as user, we need to manually go to $(git rev-parse --show-toplevel)
    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                            stdout=subprocess.PIPE, universal_newlines=True)
    assert result.returncode == 0, 'not a git repo!'
    return result.stdout.strip()


def path_to_config_file():
    return os.path.join(git_root_path(), '.summarynb.config.tsv')

def path_to_hook():
    githooks_dir = os.path.join(git_root_path(), '.git/hooks')
    assert os.path.isdir(githooks_dir), 'not a git repo!'
    return os.path.join(githooks_dir, 'pre-commit')

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
            'This will overwrite existing pre-commit hook. Do you want to continue?', abort=True)
    with open(fname, 'w') as w:
        w.write(hook_template)
        # owner has all permissions including execute
        # group and others have read
        os.chmod(fname, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    print('installed')


@main.command()
def uninstall():
    fname = path_to_hook()
    # check whether there's already a hook
    if not os.path.exists(fname):
        print('no hook installed')
        sys.exit(1)
    if click.confirm('This will remove all pre-commit hooks. Do you want to continue?'):
        os.remove(fname)
        print('uninstalled')


def get_or_create_metadata():
    # retrieves or creates metadata file
    pass


def write_metadata():
    # writes metadata file
    pass


@main.command()
def list_nb():
    # TODO: reports which notebooks are registered for autorun, and whether they are found on disk
    pass


def prune_nb():
    # TODO: prunes missing notebooks for autorun list
    pass


@main.command()
def register_nb():
    # TODO: registers a notebook for autorun
    pass


@main.command()
def unregister_nb():
    # TODO: deregisters a notebook for autorun
    pass


@main.command()
def run():
    # TODO: execute notebooks in autorun list
    print('ran hook')


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
