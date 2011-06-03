from django.contrib.staticfiles.finders import BaseStorageFinder

from pipeline.storage import CompressStorage


class CompressFinder(BaseStorageFinder):
    storage = CompressStorage
