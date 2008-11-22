import os

from compress.utils import get_output_filename, media_root
from compress.versioning.base import VersioningBase

def max_mtime(files):
    return int(max([os.stat(media_root(f)).st_mtime for f in files]))

class MTimeVersioning(VersioningBase):
    
    def get_version(self, source_files):
        mtime = max_mtime(source_files)
        try:
            return str(int(mtime))
        except ValueError:
            return str(mtime)
        
    def needs_update(self, output_file, source_files, version):

        output_file_name = get_output_filename(output_file, version)
        compressed_file_full = media_root(output_file_name)

        return (os.stat(compressed_file_full).st_mtime < version), version
            
        