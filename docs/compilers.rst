.. _ref-compilers:

=========
Compilers
=========


Coffee Script compiler
======================

The Coffee Script compiler use `Coffee Script <http://jashkenas.github.com/coffee-script/>`_
to compile your javascripts.

To use it add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
  )

``PIPELINE_COFFEE_SCRIPT_BINARY``
---------------------------------

  Command line to execute for coffee program.
  You will most likely change this to the location of coffee on your system.

  Defaults to ``'/usr/local/bin/coffee'``.

``PIPELINE_COFFEE_SCRIPT_ARGUMENTS``
------------------------------------
  
  Additional arguments to use when coffee is called.
  
  Defaults to ``''``.

LESS compiler
=============

The LESS compiler use `LESS <http://lesscss.org/>`_
to compile your stylesheets.

To use it add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
  )

``PIPELINE_LESS_BINARY``
------------------------

  Command line to execute for lessc program.
  You will most likely change this to the location of lessc on your system.

  Defaults to ``'/usr/local/bin/lessc'``.

``PIPELINE_LESS_ARGUMENTS``
---------------------------

  Additional arguments to use when lessc is called.

  Defaults to ``''``.

SASS compiler
=============

The SASS compiler use `SASS <http://sass-lang.com/>`_
to compile your stylesheets.

To use it add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
    'pipeline.compilers.sass.SASSCompiler',
  )


``PIPELINE_SASS_BINARY``
------------------------
  
  Command line to execute for sass program.
  You will most likely change this to the location of sass on your system.

  Defaults to ``'/usr/local/bin/sass'``.

``PIPELINE_SASS_ARGUMENTS``
---------------------------
  
  Additional arguments to use when sass is called.

  Defaults to ``''``.


Stylus compiler
===============

The Stylus compiler use `Stylus <http://learnboost.github.com/stylus/>`
to compile your stylesheets.

To use it add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
      'pipeline.compilers.stylus.StylusCompiler',
  )


``PIPELINE_STYLUS_BINARY``
--------------------------

  Command line to execute for stylus program.
  You will most likely change this to the location of stylus on your system.
 
  Defaults to ``'/usr/local/bin/stylus'``.

``PIPELINE_STYLUS_ARGUMENTS``
-----------------------------

  Additional arguments to use when stylus is called.
  
  Defaults to ``''``.



Write your own compiler class
=============================

To write your own compiler class, for example want to implement other types
of compilers.

All you need to do is to create a class that inherits from ``pipeline.compilers.CompilerBase``
and implements ``match_file`` and ``compile_file`` when needed.

Finally, specify it in the tuple of compilers ``PIPELINE_COMPILERS`` in the settings.

Example
-------

A custom compiler for a imaginary compiler called jam ::

  from pipeline.compilers import CompilerBase
  
  class JamCompiler(CompilerBase):
    output_extension = 'js'
    
    def match_file(self, filename):
      return path.endswith('.jam')
    
    def compile_file(self, content, path):
      return jam.compile(content)

