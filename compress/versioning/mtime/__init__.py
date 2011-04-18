import os

from compress.versioning import VersioningBase


class MTimeVersioning(VersioningBase):
    def version(self, paths):
        # Return the modification time for the newest source file
        return str(max(
            [int(os.stat(path).st_mtime) for path in paths]
        ))

    def need_update(self, output_file, paths, version):
        output_filename = self.output_filename(output_file, version)
        return (int(os.stat(output_filename).st_mtime) < int(version)), version
