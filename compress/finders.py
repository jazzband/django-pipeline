from django.contrib.staticfiles.finders import BaseStorageFinder

from compress.storage import CompressStorage


class CompressFinder(BaseStorageFinder):
    storage = CompressStorage
