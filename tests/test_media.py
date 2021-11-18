#!/usr/bin/env python

import summarynb


def test_image_dimensions():
    assert "max-width: inherit; max-height: inherit;" in summarynb.image("test.png")(
        None, None
    )
    assert "max-width: 800px; max-height: 800px;" in summarynb.image("test.png")(
        800, 800
    )


def test_plaintext():
    assert summarynb.plaintext("Test")() == "<pre>Test</pre>"


def test_textfile():
    assert summarynb.textfile("tests/data/test.txt")() == "<pre>Test from file\n</pre>"


def test_empty():
    assert summarynb.empty(width=None)(800) == '<div style="min-width: 800px;"></div>'
    assert summarynb.empty(width=1600)(800) == '<div style="min-width: 1600px;"></div>'
