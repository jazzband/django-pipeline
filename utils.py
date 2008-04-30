import os

from compress.conf import settings
from django.conf import settings as django_settings

def get_filter(compressor_class):
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
    return os.path.join(django_settings.MEDIA_ROOT, filename)

def media_url(filename):
    return django_settings.MEDIA_URL + filename

def write_tmpfile(content):
    try:
        filename = os.tmpnam()
    except RuntimeWarning:
        pass

    fd = open(filename, 'w+')
    fd.write(content)
    fd.close()
    return filename

def read_tmpfile(filename, delete=True):
    fd = open(filename, 'r')
    r = fd.read()
    fd.close()

    if delete:
        os.unlink(filename)

    return r

def concat(filenames, separator=''):
    r = ''

    for filename in filenames:
        fd = open(media_root(filename), 'r')
        r += fd.read()
        r += separator
        fd.close()

    return r
          
def save_file(filename, contents):
    fd = open(media_root(filename), 'w+')
    fd.write(contents)
    fd.close()

def filter_css(css, verbose=False):
    output = concat(css['source_filenames'])

    for f in settings.COMPRESS_CSS_FILTERS:
        output = get_filter(f)(verbose=verbose).filter_css(output)

    save_file(css['output_filename'], output)

def filter_js(js, verbose=False):
    output = concat(js['source_filenames'], ';') # add a ; between each files to make sure every file is properly "closed"

    for f in settings.COMPRESS_JS_FILTERS:
        output = get_filter(f)(verbose=verbose).filter_js(output)

    save_file(js['output_filename'], output)