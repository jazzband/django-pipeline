.. _ref-farfutureexpires:

==================
Far future expires
==================

Details about the "Far future expires" technique, and how to implement it with help from Pipeline

General details and considerations about the "Far future expires" technique
===========================================================================

If you really want to make sure that your CSS and JavaScript files get cached by
the browser (and possibly by proxies), you should use "Far Future Expires".
This means that you send the Expires HTTP-header with a date that is far in the future,
resulting in the file being cached at the client (almost) forever

If you do not specify an Expires header, the files will be requested again,
and the server will respond "*304 Not Modified*" - which means that the file that
the client got in its cache is still up-to-date. *However, a HTTP request will still be made anyway.*
The actual data does not get sent, but there will still be unnecessary HTTP requests, which can be avoided.

Most modern browser implement "*Heuristic expiration*", so it will actually not be
"*304 Not Modified*" for your static files on every request, however, the
`HTTP specification does not specify <http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html>`_ (see section 13.2.2)
how "*Heuristic expiration*" should be handled by the browsers.
Therefore it is recommended to explicitly set the Expires header, to make sure all
browsers cache the files in the preferred way.

This technique obviously has a drawback, when you want to change your files,
you need to change their names, since their URLs will be cached... that's right: forever!
The solution to that is pretty obvious too: change the URLs.

Versionning 
===========

If you specify ``PIPELINE_VERSION`` in your configuration, you can add a placeholder
to the filenames to output the version number of the different files.

The filename itself will be changed when any of the source files are updated.

See :doc:`configuration` for more information.

Configuration of web server
===========================

Apache
------

Expires-control in Apache is handled by mod_expires:

See documentation for more information:

* `mod_expires <http://httpd.apache.org/docs/2.2/mod/mod_expires.html>`_

For example ::

    <Directory /your/media/root/css>
        ExpiresActive on
        ExpiresDefault "access plus 10 years"
    </Directory>

Apache also allows the specify files by their mime-type ::

  ExpiresActive On
  ExpiresByType text/css "access plus 10 years"
  ExpiresByType application/x-javascript "access plus 10 years"

lighttpd
--------

lighttpd handles Expires similar to Apache, with a module called mod_expire.

* `mod_expire <http://trac.lighttpd.net/trac/wiki/Docs%3AModExpire>`_

For example, set far future headers on all files under ``/media/css/`` and ``/media/js/`` ::

    $HTTP["url"] =~ "^/media/css/" {
      expire.url = ( "" => "access 10 years" )
    }

    $HTTP["url"] =~ "^/media/js/" {
      expire.url = ( "" => "access 10 years" )
    }

nginx
-----

nginx's ``ngx_http_headers_module`` provides the ``expires`` option, which control
the ``Expires`` and ``Cache-Control`` HTTP headers.

* `ngx_http_headers_module <http://wiki.codemongers.com/NginxHttpHeadersModule>`_

For example, this will set expiration to the maximum expiration ::

   location /media/js {
      expires max;
   }

   location /media/css {
      expires max;
   }
