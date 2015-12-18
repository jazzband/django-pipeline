.. _ref-templates:

====================
Javascript Templates
====================

Pipeline allows you to use javascript templates along with your javascript views.
To use your javascript templates, just add them to your ``JAVASCRIPT`` group ::

  PIPELINE['JAVASCRIPT'] = {
    'application': {
      'source_filenames': (
        'js/application.js',
        'js/templates/**/*.jst',
      ),
      'output_filename': 'js/application.js'
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

By default, Pipeline uses a variant of `Micro Templating <http://ejohn.org/blog/javascript-micro-templating/>`_ to compile the templates, but you can choose your preferred JavaScript templating engine by changing ``PIPELINE['TEMPLATE_FUNC']`` ::

  PIPELINE['TEMPLATE_FUNC'] = 'template'

Template namespace
..................

Your templates are made available in a top-level object, by default ``window.JST``,
but you can choose your own via ``PIPELINE['TEMPLATE_NAMESPACE']`` ::

  PIPELINE['TEMPLATE_NAMESPACE'] = 'window.Template'


Template extension
..................

Templates are detected by their extension, by default ``.jst``, but you can use
your own extension via ``PIPELINE['TEMPLATE_EXT']`` ::

  PIPELINE['TEMPLATE_EXT'] = '.mustache'

Template separator
..................

Templates identifier are built using a replacement for directory separator,
by default ``_``, but you specify your own separator via ``PIPELINE['TEMPLATE_SEPARATOR']`` ::

  PIPELINE['TEMPLATE_SEPARATOR'] = '/'


Using it with your favorite template library
--------------------------------------------

Mustache
........

To use it with `Mustache <https://github.com/janl/mustache.js>`_ you will need
some extra javascript ::

  Mustache.template = function(templateString) {
    return function() {
      if (arguments.length < 1) {
        return templateString;
      } else {
        return Mustache.to_html(templateString, arguments[0], arguments[1]);
      }
    };
  };

And use these settings ::

 PIPELINE['TEMPLATE_EXT'] = '.mustache'
 PIPELINE['TEMPLATE_FUNC'] = 'Mustache.template'

Handlebars
..........

To use it with `Handlebars <http://handlebarsjs.com/>`_, use the following settings ::

 PIPELINE['TEMPLATE_EXT'] = '.handlebars'
 PIPELINE['TEMPLATE_FUNC'] = 'Handlebars.compile'
 PIPELINE['TEMPLATE_NAMESPACE'] = 'Handlebars.templates'

Ember.js + Handlebars
.....................

To use it with `Ember.js <http://emberjs.com/>`_, use the following settings ::

 PIPELINE['TEMPLATE_EXT'] = '.handlebars'
 PIPELINE['TEMPLATE_FUNC'] = 'Ember.Handlebars.compile'
 PIPELINE['TEMPLATE_NAMESPACE'] = 'window.Ember.TEMPLATES'
 PIPELINE['TEMPLATE_SEPARATOR'] = '/'

Prototype
.........

To use it with `Prototype <http://www.prototypejs.org/>`_, just setup your
``PIPELINE['TEMPLATE_FUNC']`` ::

  PIPELINE['TEMPLATE_FUNC'] = 'new Template'

