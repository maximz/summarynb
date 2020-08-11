#!/usr/bin/env python

import summarynb
import requests
import os

def test_version_number_not_yet_on_pypi():
    """For release branches, check that the version number is not yet on PyPI, so we remember to bump the version number.
    Run only on pull request builds against master branch. (Not run on push builds of master branch itself)

    PyPI API docs:
    - https://warehouse.pypa.io/api-reference/json/

    Environment variable docs:
    - https://unhashable.com/getting-the-current-branch-name-during-a-pull-request-in-travis-ci/
    - https://docs.travis-ci.com/user/environment-variables
    """
    is_pr = os.environ.get("TRAVIS_PULL_REQUEST", "false") != "false"
    targets_master = os.environ.get("TRAVIS_BRANCH", "") == "master"

    if is_pr and targets_master:
        # if the release does not exist yet, this version-specific lookup should 404
        assert (
            requests.get(
                "https://pypi.org/pypi/summarynb/{}/json".format(summarynb.__version__)
            ).status_code
            == 404
        ), "This version number already exists on pypi."