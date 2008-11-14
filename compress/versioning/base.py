class VersioningBase(object):
    def __init__(self, verbose):
        self.verbose = verbose

    def get_version(self, source_files):
        raise NotImplementedError
        
    def needs_update(self, output_file, source_files, version):
        raise NotImplementedError
        
class VersioningError(Exception):
    """
    This exception is raised when version creation fails
    """
    pass