PackageNotFoundError = None
try:
    from importlib.metadata import PackageNotFoundError, version as get_version
except ImportError:
    get_version = None

if get_version is None:
    try:
        from pkg_resources import DistributionNotFound as PackageNotFoundError, get_distribution


        def get_version(x):
            return get_distribution(x).version
    except ImportError:
        get_version = None
        PackageNotFoundError = None
        get_distribution = None

__version__ = None
if get_version is not None:
    try:
        __version__ = get_version("django-pipeline")
    except PackageNotFoundError:
        pass
