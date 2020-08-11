#!/usr/bin/env python

"""Tests for `summarynb` package."""

import pytest

from click.testing import CliRunner

import summarynb
from summarynb import cli

# TODO: Test _make_HTML() end-to-end against snapshotted reference html
# TODO: Test _get_template()


def test_chunks():
    # should flatten
    # should accept weird shapes
    # really this should be a pytest fixture with separate functions for each, but keeping quick and dirty for now
    test_input = [["a", "b"], ["c", "d"], ["e", "filename"]]
    assert summarynb.chunks(test_input, (3, 2)) == test_input, "Reshape failed"
    assert summarynb.chunks(test_input, (2, 3)) == [
        ["a", "b", "c"],
        ["d", "e", "filename"],
    ], "Reshape failed"
    assert summarynb.chunks(test_input, (1, 6)) == [
        ["a", "b", "c", "d", "e", "filename"]
    ], "Reshape failed"
    assert (
        summarynb.chunks(test_input, (2)) == test_input
    ), "Should accept non-tuple shape"
    assert (
        summarynb.chunks(test_input, 2) == test_input
    ), "Should accept non-tuple shape"
    assert summarynb.chunks(test_input, 4) == [
        ["a", "b", "c", "d"],
        ["e", "filename"],
    ], "Allow mis-shaped row overflow"
    with pytest.raises(AssertionError):
        summarynb.chunks(test_input, (2, 2))


def test_flatten():
    assert (
        summarynb._flatten([["file1", "file2", "file3"]])
        == summarynb._flatten(["file1", "file2", "file3"])
        == summarynb._flatten(["file1", ["file2", ["file3"]]])
        == ["file1", "file2", "file3"]
    )


def test_chunks_accept_flat_list():
    # should accept list, not just list of lists
    assert summarynb.chunks(["file1", "file2", "file3"], 2) == [
        ["file1", "file2"],
        ["file3"],
    ]


def test_list_of_lists_from_object():
    assert summarynb._ensure_list_of_lists("a") == [["a"]]


def test_list_of_lists_from_list():
    assert summarynb._ensure_list_of_lists(["a"]) == [["a"]]


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "Summary Notebooks Tool" in result.output
    assert "--help  Show this message and exit." in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


def test_read_write_metadata_consistency():
    """Read/write metadata several times. Confirm consistent."""
    df1 = cli.get_or_create_metadata()
    cli.write_metadata(df1)
    df2 = cli.get_or_create_metadata()
    cli.write_metadata(df2)
    df3 = cli.get_or_create_metadata()
    assert df1.equals(df2)
    assert df2.equals(df3)
