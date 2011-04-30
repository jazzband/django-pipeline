.. _ref-versioning:

==========
Versioning
==========

There are several ways for generating version strings. Basically, two types are available.
These are: mtime version strings and hash version strings.

mtime version strings (default)
===============================

This is the default method for generating version strings. In short, when invoked, it checks whether any of the source files system timestamps (mtime) is newer than the version string of the corresponding compressed file. If that is the case, the compressed output file version string will be the mtime of the most recent source file.

hash version strings
====================

Hash-based versioning works by generating a hash string based on the contents of the source files. Available hash-based versioning methods are MD5 and SHA-1.

MD5 version strings
-------------------

To generate MD5 version strings, put this in your `settings.py` ::

    COMPRESS_VERSIONING = 'compress.versioning.hash.MD5Versioning'

SHA-1 version string
--------------------

To generate SHA-1 version strings, put this in your `settings.py`::

    COMPRESS_VERSIONING = 'compress.versioning.hash.SHA1Versioning'


Git version strings
===================

Versions formed on git revisions in codebase. Provides a fast way to check if any of your files changed that
will be consistent across multiple web servers so that they all generate the same version numbers for each
set of source files, assuming their git repositories are all in sync.

Assumes deployment is git repositiory. Requires GitPython 0.2.0. 
GitPython 0.3.0 uses an async library that does not currently play well with Django. To install using Git just do
pip install GitPython==0.2.0-beta1.

Git revision version strings
----------------------------

To generate versions based on revision of every file in your source file list, put this in your `settings.py`::

    COMPRESS_VERSIONING = 'compress.versioning.git.GitVersioningBase'

Git HEAD last revision version strings
--------------------------------------

To generate versions based on the latest revision of HEAD in your git repository (which assumes all of your source files are in the
same repository), put this in your `settings.py`::

    COMPRESS_VERSIONING = 'compress.versioning.git.GitHeadRevVersioning'

Write your own versioning class
===============================

To write your own versioning class, you can subclass one of the available versioning classes.

Example
-------

For example, you want a short version string based on the SHA-1 version string.
You can do this by subclassing the SHA1Versioning class and overriding its get_version() method, like this::

    from compress.versioning.hash import SHA1Versioning

    class ShortSHA1Versioning(SHA1Versioning):
        """Custom SHA1Versioning class"""
    
        def get_version(self, source_files):
            """Return the first 10 characters of the SHA-1 version string"""
            version = super(ShortSHA1Versioning, self).get_version(source_files)
            return version[:10]

In your ``settings.py`` add::

    COMPRESS_VERSIONING = 'app.module.ShortSHA1Versioning'

.. note::

  Replace ``app`` and ``module`` by the app and module that contains your versioning class

Production environment
======================

You probably do not want the source files to be evaluated and (if needed)
regenerated on every request in a production environment.
Especially when calculating a hash on every request could be expensive.
To avoid this, make sure your source files are compressed before deployment,
and put the following settings in your production environment's ``settings.py``::

    COMPRESS_AUTO = False
    COMPRESS_VERSION = True

This way, the names of the compressed files will be looked up in the file system, instead of being evaluated and (if needed) regenerated on every request.