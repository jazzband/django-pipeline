from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("django-pipeline")
except PackageNotFoundError:
    __version__ = None
