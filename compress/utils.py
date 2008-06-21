import os
import re

from django.conf import settings as django_settings
from django.utils.http import urlquote
from django.dispatch import dispatcher

from compress.conf import settings
from compress.signals import css_filtered, js_filtered

def get_filter(compressor_class):
    """
    Convert a string version of a function name to the callable object.
    """
    if not hasattr(compressor_class, '__bases__'):
        try:
            compressor_class = compressor_class.encode('ascii')
            mod_name, class_name = get_mod_func(compressor_class)
            if class_name != '':
                compressor_class = getattr(__import__(mod_name, {}, {}, ['']), class_name)
        except (ImportError, AttributeError):
            pass
    return compressor_class

def get_mod_func(callback):
    """
    Converts 'django.views.news.stories.story_detail' to
    ('django.views.news.stories', 'story_detail')
    """

    try:
        dot = callback.rindex('.')
    except ValueError:
        return callback, ''
    return callback[:dot], callback[dot+1:]

def needs_update(output_file, source_files):
    """
    Scan the source files for changes and returns True if the output_file needs to be updated.
    """

    mtime = max_mtime(source_files)
    version = get_version(mtime)

    compressed_file_full = media_root(get_output_filename(output_file, version))

    if not os.path.exists(compressed_file_full):
        return True, version

    # Check if the output file is outdated
    return (os.stat(compressed_file_full).st_mtime < mtime), mtime

def media_root(filename):
    """
    Return the full path to ``filename``. ``filename`` is a relative path name in MEDIA_ROOT
    """
    return os.path.join(django_settings.MEDIA_ROOT, filename)

def media_url(url):
    return django_settings.MEDIA_URL + urlquote(url)

def write_tmpfile(content):
    try:
        filename = os.tmpnam()
    except RuntimeWarning:
        pass

    fd = open(filename, 'wb+')
    fd.write(content)
    fd.close()
    return filename

def read_tmpfile(filename, delete=True):
    fd = open(filename, 'rb')
    r = fd.read()
    fd.close()

    if delete:
        os.unlink(filename)

    return r

def concat(filenames, separator=''):
    """
    Concatenate the files from the list of the ``filenames``, ouput separated with ``separator``.
    """
    r = ''

    for filename in filenames:
        fd = open(media_root(filename), 'rb')
        r += fd.read()
        r += separator
        fd.close()

    return r

def max_mtime(files):
    return int(max([os.stat(media_root(f)).st_mtime for f in files]))

def save_file(filename, contents):
    fd = open(media_root(filename), 'wb+')
    fd.write(contents)
    fd.close()

def get_output_filename(filename, version):
    if settings.COMPRESS_VERSION:
        return filename.replace(settings.COMPRESS_VERSION_PLACEHOLDER, version)
    else:
        return filename.replace(settings.COMPRESS_VERSION_PLACEHOLDER, settings.COMPRESS_VERSION_DEFAULT)

def get_version(mtime):
    return str(int(mtime))

def remove_files(path, filename, verbosity=0):
    regex = re.compile(r'^%s$' % (os.path.basename(get_output_filename(settings.COMPRESS_VERSION_PLACEHOLDER.join([re.escape(part) for part in filename.split(settings.COMPRESS_VERSION_PLACEHOLDER)]), r'\d+'))))

    for f in os.listdir(path):
        if regex.match(f):
            if verbosity >= 1:
                print "Removing outdated file %s" % f

            os.unlink(os.path.join(path, f))

def filter_common(obj, verbosity, filters, attr, separator, signal):
    output = concat(obj['source_filenames'], separator)
    filename = get_output_filename(obj['output_filename'], get_version(max_mtime(obj['source_filenames'])))

    if settings.COMPRESS_VERSION:
        remove_files(os.path.dirname(media_root(filename)), obj['output_filename'], verbosity)

    if verbosity >= 1:
        print "Saving %s" % filename

    for f in filters:
        output = getattr(get_filter(f)(verbose=(verbosity >= 2)), attr)(output)

    save_file(filename, output)
    dispatcher.send(signal=signal)

def filter_css(css, verbosity=0):
    return filter_common(css, verbosity, filters=settings.COMPRESS_CSS_FILTERS, attr='filter_css', separator='', signal=css_filtered)

def filter_js(js, verbosity=0):
    return filter_common(js, verbosity, filters=settings.COMPRESS_JS_FILTERS, attr='filter_js', separator=';', signal=js_filtered)