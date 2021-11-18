#!/usr/bin/env python

import summarynb
import requests
import os


def test_version_number_not_yet_on_pypi():
    """For release branches, check that the version number is not yet on PyPI, so we remember to bump the version number.
    Run only on pull request builds against master branch. (Not run on push builds of master branch itself)

    PyPI API docs:
    - https://warehouse.pypa.io/api-reference/json/
    """
    is_pr_targeting_master = (
        os.environ.get("IS_PR_TARGETING_MASTER", "false") != "false"
    )

    if is_pr_targeting_master:
        # if the release does not exist yet, this version-specific lookup should 404
        assert (
            requests.get(
                "https://pypi.org/pypi/summarynb/{}/json".format(summarynb.__version__)
            ).status_code
            == 404
        ), "This version number already exists on pypi."
