try:
    from staticfiles.finders import BaseStorageFinder
except ImportError:
    from django.contrib.staticfiles.finders import BaseStorageFinder

from pipeline.storage import PipelineFinderStorage


class PipelineFinder(BaseStorageFinder):
    storage = PipelineFinderStorage
