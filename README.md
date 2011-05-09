**django-compress** provides an automated system for compressing CSS and 
JavaScript files. By default, it only outputs compressed files while not in 
DEBUG-mode. That means you can still debug and edit your source files while 
coding, and when going to production, the compressed files will be 
automatically generated.

Support for jsmin and CSSTidy is included and enabled by default (but can 
easily be disabled). Support for YUI Compressor is also supported out of the 
box.

**django-compress** includes template tags for outputting the URLs to the 
CSS/JavaScript?-files and some other goodies to improve the performance of 
serving static media.

**django-compress** [code][] and [documentation][] is available at [github][].

[github]: http://github.com/
[code]: http://github.com/pelme/django-compress/tree/master
[documentation]: http://github.com/pelme/django-compress/tree/master/docs
