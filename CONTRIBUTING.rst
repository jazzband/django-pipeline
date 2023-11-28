.. image:: https://jazzband.co/static/img/jazzband.svg
   :target: https://jazzband.co/
   :alt: Jazzband

This is a `Jazzband <https://jazzband.co>`_ project. By contributing you agree to abide by the `Contributor Code of Conduct <https://jazzband.co/docs/conduct>`_ and follow the `guidelines <https://jazzband.co/docs/guidelines>`_.

Contribute
==========

#. Check for open issues or open a fresh issue to start a discussion around a
   feature idea or a bug. There is a **contribute!** tag for issues that should be
   ideal for people who are not very familiar with the codebase yet.
#. Fork the repository on Github to start making your changes on a topic branch.
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published.
   Make sure to add yourself to *AUTHORS*.

Otherwise, if you simply wants to suggest a feature or report a bug, create an issue :
https://github.com/jazzband/django-pipeline/issues


Running tests
=============

We use tox to run the test suite on different versions locally (and GitHub Actions
to automate the check for PRs).

To tun the test suite locally, please make sure your python environment has
tox and django installed::

    python3.7 -m pip install tox

Since we use a number of node.js tools, one should first install the node
dependencies. We recommend using [nvm](https://github.com/nvm-sh/nvm#installation-and-update) , tl;dr::

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.2/install.sh | bash
    nvm install node
    nvm use node

And then simply execute tox to run the whole test matrix::

    tox
