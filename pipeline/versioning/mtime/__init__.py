import time

from pipeline.storage import storage
from pipeline.versioning import VersioningBase


class MTimeVersioning(VersioningBase):
    def version(self, paths):
        # Return the modification time for the newest source file
        return str(max(
            [int(time.mktime(storage.modified_time(path).timetuple())) for path in paths]
        ))

    def need_update(self, output_file, paths, version):
        output_filename = self.output_filename(output_file, version)
        try:
            modified_time = storage.modified_time(output_filename)
        except Exception:
            return True, version
        return (int(time.mktime(modified_time.timetuple())) < int(version)), version
