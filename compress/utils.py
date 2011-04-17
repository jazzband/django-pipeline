import os
import re

from django.conf import settings as django_settings
from django.utils.http import urlquote

from compress.conf import settings
from compress.signals import css_filtered, js_filtered


def get_class(class_string):
    """
    Convert a string version of a function name to the callable object.
    """
    if not hasattr(class_string, '__bases__'):
        try:
            class_string = class_string.encode('ascii')
            mod_name, class_name = get_mod_func(class_string)
            if class_name != '':
                class_string = getattr(__import__(mod_name, {}, {}, ['']), class_name)
        except (ImportError, AttributeError):
            raise Exception('Failed to import filter %s' % class_string)
    return class_string


def get_mod_func(callback):
    """
    Converts 'django.views.news.stories.story_detail' to
    ('django.views.news.stories', 'story_detail')
    """
    try:
        dot = callback.rindex('.')
    except ValueError:
        return callback, ''
    return callback[:dot], callback[dot + 1:]


def get_hexdigest(plaintext):
    """
    Create a hexdigest from a plaintext string
    """
    try:
        import hashlib
        return hashlib.sha1(plaintext).hexdigest()
    except ImportError:
        import sha
        return sha.new(plaintext).hexdigest()


def needs_update(output_file, source_files, verbosity=0):
    """
    Scan the source files for changes and returns True if the output_file needs to be updated.
    """

    version = get_version(source_files)

    on = get_output_filename(output_file, version)
    compressed_file_full = compress_root(on)

    if not os.path.exists(compressed_file_full):
        return True, version

    update_needed = getattr(get_class(settings.COMPRESS_VERSIONING)(), 'needs_update')(output_file, source_files, version)
    return update_needed


def compress_root(filename):
    """
    Return the full path to ``filename``. ``filename`` is a relative path name in COMPRESS_ROOT
    """
    return os.path.join(settings.COMPRESS_ROOT, filename)


def compress_source(filename):
    """
    Return the full path to ``filename``. ``filename`` is a relative path name in COMPRESS_SOURCE
    """
    return os.path.join(settings.COMPRESS_SOURCE, filename)


def compress_url(url, prefix=None):
    if prefix:
        return prefix + urlquote(url)
    return settings.COMPRESS_URL + urlquote(url)


def concat(filenames, separator=''):
    """
    Concatenate the files from the list of the ``filenames``, output separated with ``separator``.
    """
    # find relative paths in css:
    # url definition, any spacing, single or double quotes, no starting slash
    rel_exp = re.compile(
        '(url\s*\(\s*[\'"]?\s*)([^/\'"\s]\S+?)(\s*[\'"]?\s*\))',
        flags=re.IGNORECASE)
    r = ''
    for filename in filenames:
        fd = open(compress_source(filename), 'rb')
        contents = fd.read()
        fd.close()
        if filename.lower().endswith('.css') and \
            django_settings.COMPRESS_ROOT == settings.COMPRESS_SOURCE:
            if django_settings.COMPRESS_URL.endswith('/'):
                abspath = os.path.normpath(os.path.dirname(filename))
            else:
                abspath = os.path.normpath(os.path.join('/',
                                                    os.path.dirname(filename)))
            abspath = django_settings.COMPRESS_URL + abspath + '/'
            contents = rel_exp.sub('\\1' + abspath + '\\2\\3', contents)
        r += contents
        r += separator
    return r


def save_file(filename, contents):
    dirname = os.path.dirname(compress_root(filename))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    fd = open(compress_root(filename), 'wb+')
    fd.write(contents)
    fd.close()


def get_output_filename(filename, version):
    if settings.COMPRESS_VERSION and version is not None:
        return filename.replace(settings.COMPRESS_VERSION_PLACEHOLDER, version)
    else:
        return filename.replace(settings.COMPRESS_VERSION_PLACEHOLDER, settings.COMPRESS_VERSION_DEFAULT)


def get_version(source_files, verbosity=0):
    version = getattr(get_class(settings.COMPRESS_VERSIONING)(), 'get_version')(source_files)
    return version


def get_version_from_file(path, filename):
    regex = re.compile(r'^%s$' % (get_output_filename(settings.COMPRESS_VERSION_PLACEHOLDER.join([re.escape(part) for part in filename.split(settings.COMPRESS_VERSION_PLACEHOLDER)]), r'([A-Za-z0-9]+)')))
    results = []
    for f in sorted(os.listdir(path), reverse=True):
        result = regex.match(f)
        if result and result.groups():
            results.append(result.groups()[0])
    results.sort()
    return results[-1]


def remove_files(path, filename, verbosity=0):
    regex = re.compile(r'^%s$' % (os.path.basename(get_output_filename(settings.COMPRESS_VERSION_PLACEHOLDER.join([re.escape(part) for part in filename.split(settings.COMPRESS_VERSION_PLACEHOLDER)]), r'[A-Za-z0-9]+'))))
    if os.path.exists(path):
        for f in os.listdir(path):
            if regex.match(f):
                if verbosity >= 1:
                    print "Removing outdated file %s" % f

                os.unlink(os.path.join(path, f))


def filter_common(obj, verbosity, filters, attr, separator, signal):
    output = concat(obj['source_filenames'], separator)

    filename = get_output_filename(obj['output_filename'], get_version(obj['source_filenames']))

    if settings.COMPRESS_VERSION and settings.COMPRESS_VERSION_REMOVE_OLD:
        remove_files(os.path.dirname(compress_root(filename)), obj['output_filename'], verbosity)

    if verbosity >= 1:
        print "Saving %s" % filename

    for f in filters:
        output = getattr(get_class(f)(verbose=(verbosity >= 2)), attr)(output)

    save_file(filename, output)
    signal.send(None)


def filter_css(css, verbosity=0):
    return filter_common(css, verbosity, filters=settings.COMPRESS_CSS_FILTERS, attr='filter_css', separator='', signal=css_filtered)


def filter_js(js, verbosity=0):
    return filter_common(js, verbosity, filters=settings.COMPRESS_JS_FILTERS, attr='filter_js', separator='', signal=js_filtered)
