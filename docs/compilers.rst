.. _ref-compilers:

=========
Compilers
=========


Coffee Script compiler
======================

The Coffee Script compiler uses `Coffee Script <http://jashkenas.github.com/coffee-script/>`_
to compile your javascripts.

To use it add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
  )

``PIPELINE_COFFEE_SCRIPT_BINARY``
---------------------------------

  Command line to execute for coffee program.
  You will most likely change this to the location of coffee on your system.

  Defaults to ``'/usr/bin/env coffee'``.

``PIPELINE_COFFEE_SCRIPT_ARGUMENTS``
------------------------------------

  Additional arguments to use when coffee is called.

  Defaults to ``''``.

Live Script compiler
======================

The LiveScript compiler uses `LiveScript <https://github.com/gkz/LiveScript>`_
to compile your javascripts.

To use it add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
    'pipeline.compilers.livescript.LiveScriptCompiler',
  )

``PIPELINE_LIVE_SCRIPT_BINARY``
---------------------------------

  Command line to execute for LiveScript program.
  You will most likely change this to the location of lsc on your system.

  Defaults to ``'/usr/bin/env lsc'``.

``PIPELINE_LIVE_SCRIPT_ARGUMENTS``
------------------------------------

  Additional arguments to use when lsc is called.

  Defaults to ``''``.

LESS compiler
=============

The LESS compiler uses `LESS <http://lesscss.org/>`_
to compile your stylesheets.

To use it add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
  )

``PIPELINE_LESS_BINARY``
------------------------

  Command line to execute for lessc program.
  You will most likely change this to the location of lessc on your system.

  Defaults to ``'/usr/bin/env lessc'``.

``PIPELINE_LESS_ARGUMENTS``
---------------------------

  Additional arguments to use when lessc is called.

  Defaults to ``''``.

SASS compiler
=============

The SASS compiler uses `SASS <http://sass-lang.com/>`_
to compile your stylesheets.

To use it add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
    'pipeline.compilers.sass.SASSCompiler',
  )


``PIPELINE_SASS_BINARY``
------------------------

  Command line to execute for sass program.
  You will most likely change this to the location of sass on your system.

  Defaults to ``'/usr/bin/env sass'``.

``PIPELINE_SASS_ARGUMENTS``
---------------------------

  Additional arguments to use when sass is called.

  Defaults to ``'--update'``.


Stylus compiler
===============

The Stylus compiler uses `Stylus <http://learnboost.github.com/stylus/>`_
to compile your stylesheets.

To use it add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
      'pipeline.compilers.stylus.StylusCompiler',
  )


``PIPELINE_STYLUS_BINARY``
--------------------------

  Command line to execute for stylus program.
  You will most likely change this to the location of stylus on your system.

  Defaults to ``'/usr/bin/env stylus'``.

``PIPELINE_STYLUS_ARGUMENTS``
-----------------------------

  Additional arguments to use when stylus is called.

  Defaults to ``''``.



Write your own compiler class
=============================

You can write your own compiler class, for example if you want to implement other types
of compilers.

To do so, you just have to create a class that inherits from ``pipeline.compilers.CompilerBase``
and implements ``match_file`` and ``compile_file`` when needed.

Finally, specify it in the tuple of compilers ``PIPELINE_COMPILERS`` in the settings.

Example
-------

A custom compiler for an imaginary compiler called jam ::

  from pipeline.compilers import CompilerBase

  class JamCompiler(CompilerBase):
    output_extension = 'js'

    def match_file(self, filename):
      return filename.endswith('.jam')

    def compile_file(self, infile, outfile, outdated=False, force=False):
      if not outdated and not force:
        return  # No need to recompiled file
      return jam.compile(infile, outfile)


3rd Party Compilers
===================

Here is an (in)complete list of 3rd party compilers that integrate with django-pipeline

Compass (requires RubyGem)
--------------------------

:Creator:
    `Mila Labs <https://github.com/mila-labs>`_
:Description:
    Compass compiler for django-pipeline using the original Ruby gem.
:Link:
    `https://github.com/mila-labs/django-pipeline-compass-rubygem`

Compass (standalone)
--------------------

:Creator:
    `Vitaly Babiy <https://github.com/vbabiy>`_
:Description:
    django-pipeline-compass is a compiler for `django-pipeline <https://github.com/cyberdelia/django-pipeline>`_. Making it really easy to use scss and compass with out requiring the compass gem.
:Link:
    `https://github.com/vbabiy/django-pipeline-compass`
