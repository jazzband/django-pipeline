Pipeline
========

.. image:: https://jazzband.co/static/img/badge.svg
    :alt: Jazzband
    :target: https://jazzband.co/

.. image:: https://github.com/jazzband/django-pipeline/workflows/Test/badge.svg
   :target: https://github.com/jazzband/django-pipeline/actions
   :alt: GitHub Actions

.. image:: https://codecov.io/gh/jazzband/django-pipeline/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jazzband/django-pipeline
   :alt: Coverage

.. image:: https://readthedocs.org/projects/django-pipeline/badge/?version=latest
    :alt: Documentation Status
    :target: https://django-pipeline.readthedocs.io/en/latest/?badge=latest


Pipeline is an asset packaging library for Django, providing both CSS and
JavaScript concatenation and compression, built-in JavaScript template support,
and optional data-URI image and font embedding.

.. image:: https://github.com/jazzband/django-pipeline/raw/master/img/django-pipeline.svg
   :alt: Django Pipeline Overview


Installation
------------

To install it, simply:

.. code-block:: bash

    pip install django-pipeline


Quickstart
----------

Pipeline compiles and compress your assets files from
``STATICFILES_DIRS`` to your ``STATIC_ROOT`` when you run Django's
``collectstatic`` command.

These simple steps add Pipeline to your project to compile multiple ``.js`` and
``.css`` file into one and compress them.

Add Pipeline to your installed apps:

.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
        ...
        'pipeline',
    ]


Use Pipeline specified classes for ``STATICFILES_FINDERS`` and ``STATICFILES_STORAGE``:

.. code-block:: python

    STATICFILES_STORAGE = 'pipeline.storage.PipelineManifestStorage'

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'pipeline.finders.PipelineFinder',
    )


Configure Pipeline:

.. code-block:: python

    # The folowing config merges CSS files(main.css, normalize.css)
    # and JavaScript files(app.js, script.js) and compress them using
    # `yuglify` into `css/styles.css` and `js/main.js`
    # NOTE: Pipeline only works when DEBUG is False
    PIPELINE = {
        'STYLESHEETS': {
            'css_files': {
                'source_filenames': (
                    'css/main.css',
                    'css/normalize.css',
                ),
                'output_filename': 'css/styles.css',
                'extra_context': {
                    'media': 'screen,projection',
                },
            },
        },
        'JAVASCRIPT': {
            'js_files': {
                'source_filenames': (
                    'js/app.js',
                    'js/script.js',
                ),
                'output_filename': 'js/main.js',
            }
        }
    }


Then, you have to install compilers and compressors binary manually.

For example, you can install them using `NPM <https://www.npmjs.com/>`_
and address them from ``node_modules`` directory in your project path:

.. code-block:: python

    PIPELINE.update({
        'YUGLIFY_BINARY': path.join(BASE_DIR, 'node_modules/.bin/yuglify'),
    })
    # For a list of all supported compilers and compressors see documentation


Load static files in your template:

.. code-block::

    {% load pipeline %}
    {% stylesheet 'css_files' %}
    {% javascript 'js_files' %}


Documentation
-------------

For documentation, usage, and examples, see:
https://django-pipeline.readthedocs.io


Issues
------
You can report bugs and discuss features on the `issues page <https://github.com/jazzband/django-pipeline/issues>`_.


Changelog
---------

See `HISTORY.rst <https://github.com/jazzband/django-pipeline/blob/master/HISTORY.rst>`_.
