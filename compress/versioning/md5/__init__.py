import cStringIO
import md5
import os

from compress.conf import settings

from compress.utils import concat, get_output_filename
from compress.versioning.base import VersioningBase

def get_md5(f, CHUNK=2**16):
    m = md5.new()
    while 1:
        chunk = f.read(CHUNK)
        if not chunk:
            break
        m.update(chunk)
    return m.hexdigest()

class MD5Versioning(VersioningBase):
    
    def get_version(self, source_files):
        buf = concat(source_files)
        s = cStringIO.StringIO(buf)
        version = get_md5(s)
        s.close()
        return version
        
    def needs_update(self, output_file, source_files, version):
        output_file_name = get_output_filename(output_file, version)
        ph = settings.COMPRESS_VERSION_PLACEHOLDER
        of = output_file
        try:
            phi = of.index(ph)
            old_version = output_file_name[phi:phi+len(ph)-len(of)]
            return (version != old_version), version
        except ValueError:
            # no placeholder found, do not update, manual update if needed
            return False, version