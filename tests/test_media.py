#!/usr/bin/env python

import summarynb

def test_image_dimensions():
    assert 'max-width: inherit; max-height: inherit;' in summarynb.image('test.png')(None, None)
    assert 'max-width: 800px; max-height: 800px;' in summarynb.image('test.png')(800, 800)