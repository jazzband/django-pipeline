import os



from django.conf import settings

def get_compressor(compressor_class):
    """
    Convert a string version of a function name to the callable object.

    If the lookup_view is not an import path, it is assumed to be a URL pattern
    label and the original string is returned.

    If can_fail is True, lookup_view might be a URL pattern label, so errors
    during the import fail and the string is returned.
    """
    if not hasattr(compressor_class, '__bases__'):
        try:
            # Bail early for non-ASCII strings (they can't be functions).
            compressor_class = compressor_class.encode('ascii')
            mod_name, class_name = get_mod_func(compressor_class)
            print mod_name
            print class_name
            if class_name != '':
                compressor_class = getattr(__import__(mod_name, {}, {}, ['']), class_name)
        except (ImportError, AttributeError):
            pass
    return compressor_class

# since this function is not part of any offical API,
# it is duplicated here to avoid regressions with future/different versions
# of django
def get_mod_func(callback):
    # Converts 'django.views.news.stories.story_detail' to
    # ['django.views.news.stories', 'story_detail']
    try:
        dot = callback.rindex('.')
    except ValueError:
        return callback, ''
    return callback[:dot], callback[dot+1:]

def needs_update(compressed_file, source_files):
    """
    Scan the source files for changes and returns True if the compressed_file needs to be updated.
    compressed_file and source_files should be given with full paths
    """
    compressed_file_full = media_root(compressed_file)

    if not os.path.exists(compressed_file_full):
        return True
    compressed_file_mtime = os.stat(compressed_file_full).st_mtime

    for source_file in source_files:
        if compressed_file_mtime < os.stat(media_root(source_file)).st_mtime:
            return True

    return False

def media_root(filename):
    return os.path.join(settings.MEDIA_ROOT, filename)

def media_url(filename):
    return settings.MEDIA_URL + filename

def compress_css(css):
    get_compressor(settings.COMPRESS_CSS_COMPRESSOR)().compress_css(css)

def compress_js(js):
    get_compressor(settings.COMPRESS_JS_COMPRESSOR)().compress_js(js)