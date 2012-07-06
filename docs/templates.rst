.. _ref-templates:

====================
Javascript Templates
====================

Pipeline allows you to use javascript templates along with your javascript views.
To use your javascript templates, just add them to your ``PIPELINE_JS`` group ::

  PIPELINE_JS = {
    'application': {
      'source_filenames': (
        'js/application.js',
        'js/templates/**/*.jst',
      ),
      'output_filename': 'js/application.r?.js'
    }
  }

For example, if you have the following template ``js/templates/photo/detail.jst`` ::

  <div class="photo">
   <img src="<%= src %>" />
   <div class="caption">
    <%= caption %>
   </div>
  </div>

It will be available from your javascript code via window.JST ::

  JST.photo_detail({ src:"images/baby-panda.jpg", caption:"A baby panda is born" });


Configuration
-------------

Template function
.................

By default, Pipeline uses a variant of `Micro Templating <http://ejohn.org/blog/javascript-micro-templating/>`_ to compile the templates, but you can choose your preferred JavaScript templating engine by changing ``PIPELINE_TEMPLATE_FUNC`` ::

  PIPELINE_TEMPLATE_FUNC = 'template'

Template namespace
..................

Your templates are made available in a top-level object, by default ``window.JST``,
but you can choose your own via ``PIPELINE_TEMPLATE_NAMESPACE`` ::

  PIPELINE_TEMPLATE_NAMESPACE = 'window.Template'


Template extension
..................

Templates are detected by their extension, by default ``.jst``, but you can use
your own extension via ``PIPELINE_TEMPLATE_EXT`` ::

  PIPELINE_TEMPLATE_EXT = '.mustache'


Using it with your favorite template library
--------------------------------------------

Mustache
........

To use it with `Mustache <https://github.com/janl/mustache.js>`_ you will need
this some extra javascript ::

  Mustache.template = function(templateString) {
    return function() {
      if (arguments.length < 1) {
        return templateString;
      } else {
        return Mustache.to_html(templateString, arguments[0], arguments[1]);
      }
    };
  };

And use this settings ::

 PIPELINE_TEMPLATE_EXT = '.mustache'
 PIPELINE_TEMPLATE_FUNC = 'Mustache.template'


Prototype
.........

To use it with `Prototype <http://www.prototypejs.org/>`_, just setup your 
``PIPELINE_TEMPLATE_FUNC`` ::

  PIPELINE_TEMPLATE_FUNC = 'new Template'


Jade
....

`Jade <http://jade-lang.com/>`_ can compiles the templates to javascript for use client-side.
It does not use the PIPELINE_TEMPLATE_FUNC nor PIPELINE_TEMPLATE_EXT settings. Just have your
templates ending with the ``.jade`` extension.

To use Pipeline with Jade templates, add this to your ``PIPELINE_COMPILERS`` ::

  PIPELINE_COMPILERS = (
      'pipeline.compilers.jade.JadeCompiler',
  )

Add jade's `runtime.js <https://github.com/visionmedia/jade/blob/master/runtime.js>` (from the jade repository) and your templates to your ``PIPELINE_JS`` group ::

  PIPELINE_JS = {
    'application': {
      'source_filenames': (
        'js/application.js',
        'js/jade-runtime.js',
        'js/templates/my-template.jade',
      ),
      'output_filename': 'application.min.js'
    }
  }

Customize ``PIPELINE_TEMPLATE_NAMESPACE`` ::

  PIPELINE_TEMPLATE_NAMESPACE = 'window.JADE'

Use the template's filename on the JADE object to call the template from your javascript. Here is an example using jquery ::

  var content_html = JADE['my-template']({'awsome_template_variable': 'Here we are, born to be kings, ...'});
  $('#content').html( content_html );

`` PIPELINE_JADE_BINARY``
-------------------------

Command line program to execute for jade.
You can change this to the location of jade on your system.

Defaults to ``'/usr/bin/env jade'``.

`` PIPELINE_JADE_ARGUMENTS``
----------------------------

Additional arguments to use when jade is called.
You can disable the template's debug mode for smaller templates ::

  PIPELINE_JADE_ARGUMENTS = '-D'
