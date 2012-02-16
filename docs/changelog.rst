Changelog
=========

1.2.0
-----

 * Dropped ``synccompress`` command in favor of staticfiles ``collecstatic`` command.
 * Added file versionning via staticfiles ``CachedStaticFilesStorage``.
 * Added a default js template language.
 * Dropped ``PIPELINE_AUTO`` settings in favor of simple ``PIPELINE``.
 * Renamed ``absolute_asset_paths`` to ``absolute_paths`` for brevity.
 * Made packages lazy to avoid doing unnecessary I/O. 
