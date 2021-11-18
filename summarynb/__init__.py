import os
import pandas as pd
from IPython.display import HTML, display

"""Top-level package for Summary Notebooks."""

__author__ = """Maxim Zaslavsky"""
__email__ = "maxim@maximz.com"
__version__ = "0.1.4"

"""Functions that return functions that return HTML."""

# TODO: make max_width a property of <td>, not <img>?


def image(img_src):
    """Renders an image.

    :param img_src: Image filename.
    :type img_src: str
    :return: Template function that accepts a max pixel width integer and returns HTML.
    :rtype: function
    """

    # Convert absolute path to relative path, since a browser won't be able to grab an image from "/home/..."
    img_src = os.path.relpath(img_src)

    def template(max_width, max_height, *args, **kwargs):
        def convert_to_px_or_unset(optional_numeric_value):
            if not optional_numeric_value:
                return "inherit"
            return str(optional_numeric_value) + "px"

        max_width = convert_to_px_or_unset(max_width)
        max_height = convert_to_px_or_unset(max_height)

        return """<img src="{img_src}" style="max-width: {max_width}; max-height: {max_height};" />""".format(
            img_src=img_src, max_width=max_width, max_height=max_height
        )

    return template


def table(df):
    """Renders a Pandas dataframe.

    :param df: the dataframe
    :type df: pandas.DataFrame
    :return: Template function that returns HTML.
    :rtype: function
    """

    def template(*args, **kwargs):
        return df.to_html()

    return template


def plaintext(text, **kwargs):
    """Renders plain text.

    :param text: text to display
    :type text: str
    """

    def template(*args, **kwargs):
        # convert to html
        return f"<pre>{text}</pre>"

    return template


def empty(width=None):
    """Creates empty separator block.

    :param width: specify block width, defaults to None
    :type width: int, optional
    """

    def template(max_width, *args, **kwargs):
        # empty cell
        return f'<div style="min-width: {max_width if not width else width}px;"></div>'

    return template


"""Extensions that simplify usage of the above base functions."""


def csv(fname, cols=None, **kwargs):
    """
    Read a csv from [fname]. Optionally subset to columns [cols]. Kwargs passed onto pandas read_csv.
    """
    df = pd.read_csv(fname, **kwargs)
    if cols is not None:
        df = df[cols]
    return table(df)


def indexed_csv(fname, cols=None, **kwargs):
    """
    Read a csv from [fname], and set first column as index column. Optionally subset to columns [cols]. Kwargs passed onto pandas read_csv.
    Useful for reading in pandas series quickly.
    """
    return csv(fname, cols=cols, index_col=0, **kwargs)


def textfile(fname, **kwargs):
    """
    Read a text file and render as plain text.
    """
    with open(fname, "r") as f:
        text = f.read()
        return plaintext(text)


"""Main logic."""


def _get_template(user_input):
    """Return executable template function if not provided, based on filename."""
    if callable(user_input):
        # this is already a template function
        return user_input

    # user provided a filename
    # get extension
    extension = os.path.splitext(user_input)[1]

    # detect different table types
    if extension == ".csv":
        return csv(user_input)
    elif extension == ".tsv":
        return csv(user_input, sep="\t")
    elif extension == ".txt":
        return textfile(user_input)

    # assume it's an image
    return image(user_input)


def _ensure_list_of_lists(entries):
    """Transform input to being a list of lists."""
    if not isinstance(entries, list):
        # user passed in single object
        # wrap in a list
        # (next transformation will make this a list of lists)
        entries = [entries]
    if not any(isinstance(element, list) for element in entries):
        # user passed in a list of objects, not a list of lists
        # wrap in a list
        entries = [entries]
    return entries


def _flatten(lst):
    """Flatten sublists in list.
    see https://stackoverflow.com/a/952952/130164
    """
    from collections.abc import Sequence

    entries = []
    for sublist in lst:
        # may be a sublist
        if isinstance(sublist, Sequence) and not isinstance(
            sublist, (str, bytes, bytearray)
        ):
            # recursively flatten sublist
            entries.extend(_flatten(sublist))
        else:
            # just an item
            entries.append(sublist)
    return entries


def chunks(entries, shape):
    """Reshape [entries] into chunks of shape [shape], which can be:
    - a (number of rows, number of columns) tuple, in which case we verify length
    - or simply a number of columns, in which case we guess the right number of rows, and allow in-complete rows."""
    # Flatten entries
    entries = _flatten(entries)

    if isinstance(shape, list) or isinstance(shape, tuple):
        assert len(shape) <= 2, "Only supports 2D arrays"
        if len(shape) == 2:
            # Confirm length
            assert len(entries) == shape[0] * shape[1], "Wrong length."

    # Convert shape to (n_rows, n_cols) tuple.
    if not isinstance(shape, list) and not isinstance(shape, tuple):
        # Input was a single object.
        shape = (0, shape)
    if len(shape) == 1:
        # Input was a list of tuple of length 1.
        shape = (0, shape[0])

    n_col = shape[1]
    reshaped = [
        entries[row_num * n_col : (row_num + 1) * n_col]
        for row_num in range(len(entries) // n_col)
    ]
    if len(entries) % n_col > 0:
        # handle remainder with an uneven row
        reshaped.append(entries[(len(entries) // n_col) * n_col :])
    return reshaped


def _make_HTML(entries, headers, max_width, max_height):
    """
    Create HTML table.
    """

    def wrap_in_column(contents):
        return """<td style="text-align: center">{contents}</td>""".format(
            contents=contents
        )

    def wrap_in_row(contents):
        return """<tr>{contents}</tr>""".format(contents=contents)

    def make_headers(headers):
        if headers is not None:
            return """<tr>{contents}</tr>""".format(
                contents="\n".join(
                    [
                        """<th style="text-align: center">%s</th>"""
                        % str(header).strip()
                        for header in headers
                    ]
                )
            )
        return ""

    def wrap_in_table(contents):
        return """<table>{contents}</table>""".format(contents=contents)

    # Transform to list of lists (list of rows that are each a list of columns), if user passed in single object (1 row, 1 column) or a single list (1 row, many columns)
    entries = _ensure_list_of_lists(entries)

    # Make HTML for each row
    rows = [
        "\n".join(
            [
                wrap_in_column(_get_template(template)(max_width, max_height))
                for template in row
            ]
        )
        for row in entries
    ]
    # assemble rows into table
    return wrap_in_table(
        make_headers(headers) + "\n".join([wrap_in_row(row) for row in rows])
    )


def show(entries, headers=None, max_width=800, max_height=800):
    """
    Display chosen figures and tables in an HTML table.

    Parameters:
        - [entries]: List of rows. Each row is a list of columns. Each column is a list of executable functions that return an HTML template.
        For convenience:
            - Raw filenames (not wrapped in executable functions that return HTML templates) are also accepted, and will be auto-wrapped based on file extension.
            - If a list of lists is not provided, the input is interpreted as forming columns in a single row.

        - [headers]: List of column headers.

        - [max_width]: set max pixel width for images, default 800px. set to None to disable max width.

        - [max_height]: set max pixel height for images, default 800px. set to None to disable max height.
    """

    return display(
        HTML(
            _make_HTML(
                entries, headers=headers, max_width=max_width, max_height=max_height
            )
        )
    )
