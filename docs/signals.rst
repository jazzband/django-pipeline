.. _ref-signals:

=======
Signals
=======

A list of all signals send by pipeline.

css_compressed
--------------

**pipeline.signals.css_compressed**

	Whenever a css package is compressed, this signal is sent after the compression.

	Arguments sent with this signal :
	
		:sender:
			The ``Packager`` class that compressed the group.
		
		:package:
			The package actually compressed.
		
		:version:
			The version identifier if the newly compressed file.

js_compressed
--------------

**pipeline.signals.js_compressed**

	Whenever a js package is compressed, this signal is sent after the compression.
	
	Arguments sent with this signal :
	
		:sender:
			The ``Packager`` class that compressed the group.
		
		:package:
			The package actually compressed.
		
		:version:
			The version identifier if the newly compressed file. 
