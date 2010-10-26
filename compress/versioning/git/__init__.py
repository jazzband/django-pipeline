import os

from compress.conf import settings
from compress.utils import get_output_filename, get_hexdigest, compress_source
from compress.versioning.base import VersioningBase, VersioningError

try:
    import git
except ImportError:
    raise VersioningError("Must have GitPython package installed to use git versioning")
    
class GitVersioningBase(VersioningBase):
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

class GitRevVersioning(GitVersioningBase):
    """
    Version as hash of revision of all files in sources_files list.
    """
    def get_version(self, source_files):
        repo = git.Repo(compress_source(source_files[0]))
        kwargs = {'max_count' : 1}
        commit_revs = []
        for f in source_files:
            commit = [i for i in repo.iter_commits(paths=compress_source(f), **kwargs)][0]
            commit_revs.append(commit.name_rev)
        return get_hexdigest(', '.join(commit_revs))[0:16]

class GitHeadRevVersioning(GitVersioningBase):
    """
    Version as hash of latest revision in HEAD. Assumes all sources_files in same git repo.
    """
    def get_version(self, source_files):
        f = source_files[0]
        repo = git.Repo(compress_source(f))
        return get_hexdigest(repo.head.commit.name_rev)[0:16]