#!/usr/bin/env python

"""Tests for `summarynb` package."""

import pytest

from click.testing import CliRunner

import summarynb
from summarynb import cli

# TODO: Test _make_HTML() end-to-end against snapshotted reference html
# TODO: Test _get_template()

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_chunks():
    # should flatten
    # should accept weird shapes
    # really this should be a pytest fixture with separate functions for each, but keeping quick and dirty for now
    test_input = [['a', 'b'], ['c', 'd'], ['e', 'f']]
    assert summarynb.chunks(test_input, (3, 2)) == test_input, 'Reshape failed'
    assert summarynb.chunks(test_input, (2, 3)) == [['a', 'b', 'c'], ['d', 'e', 'f']], 'Reshape failed'
    assert summarynb.chunks(test_input, (1, 6)) == [['a', 'b', 'c', 'd', 'e', 'f']], 'Reshape failed'
    assert summarynb.chunks(test_input, (2)) == test_input, 'Should accept non-tuple shape'
    assert summarynb.chunks(test_input, 2) == test_input, 'Should accept non-tuple shape'
    assert summarynb.chunks(test_input, 4) == [['a', 'b', 'c', 'd'], ['e', 'f']], 'Allow mis-shaped row overflow'
    with pytest.raises(AssertionError):
        summarynb.chunks(test_input, (2, 2))

def test_list_of_lists_from_object():
    assert summarynb._ensure_list_of_lists('a') == [['a']]


def test_list_of_lists_from_list():
    assert summarynb._ensure_list_of_lists(['a']) == [['a']]


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'summarynb.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
