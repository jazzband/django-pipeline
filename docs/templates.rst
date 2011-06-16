.. _ref-templates:

====================
Javascript Templates
====================

Pipeline allows you to use javascript templates along with your javascript views.
To use your javascript templates, just add them to your ``COMPRESS_JS`` group ::

  COMPRESS_JS = {
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

They will be available from your javascript code via window.JST ::

  JST.photo_detail({ src:"images/baby-panda.jpg", caption:"A baby panda is born" });


Configuration
-------------

Template function
.................

By default, it use `underscore <http://documentcloud.github.com/underscore/>`_
template function, but without providing it. You can specify your own template
function via ``PIPELINE_TEMPLATE_FUNC`` ::

  PIPELINE_TEMPLATE_FUNC = 'new Template'

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

