from pipeline.conf import settings
from pipeline.storage import storage
from pipeline.versioning import VersioningBase, VersioningError

from django.utils.hashcompat import sha_constructor

try:
    import git
except ImportError:
    raise VersioningError("Must have GitPython package installed to use git versioning")


class GitVersioningBase(VersioningBase):
    def need_update(self, output_file, paths, version):
        output_file_name = self.output_filename(output_file, version)
        placeholder = settings.PIPELINE_VERSION_PLACEHOLDER
        try:
            placeholder_index = output_file.index(placeholder)
            old_version = output_file_name[placeholder_index:placeholder_index + len(placeholder) - len(output_file)]
            return (version != old_version), version
        except ValueError:
            # No placeholder found, do not update, manual update if needed
            return False, version

    def hexdigest(self, plaintext):
        return sha_constructor(plaintext).hexdigest()


class GitRevVersioning(GitVersioningBase):
    """
    Version as hash of revision of all files in sources_files list.
    """
    def version(self, paths):
        repo = git.Repo(storage.path(paths[0]))
        kwargs = {'max_count': 1}
        commit_revs = []
        for f in paths:
            f = storage.path(f)
            commit = [i for i in repo.iter_commits(paths=f, **kwargs)][0]
            commit_revs.append(commit.name_rev)
        return self.hexdigest(', '.join(commit_revs))[0:16]


class GitHeadRevVersioning(GitVersioningBase):
    """
    Version as hash of latest revision in HEAD. Assumes all sources_files in same git repo.
    """
    def version(self, paths):
        repo = git.Repo(storage.path(paths[0]))
        return self.hexdigest(repo.head.commit.name_rev)[0:16]
