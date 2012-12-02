from os.path import dirname, getmtime, normpath
from datetime import datetime
from pipeline.compilers import SubProcessCompiler

class BaseFileTree(object):
    files_info = {}

    def __init__(self, storage, name, searchpath = ['.']):
        self.storage = storage
        self.name = normpath(name)
        self.searchpath = searchpath
        self.mtime = datetime.fromtimestamp(0.0)
        self.children = None
        self.basepath = dirname(self.name)

        self.files_info[self.name] = self

    def flatlist(self, target_time, callstack = []):
        ret = [self]

        if self in callstack or not self.storage.exists(self.name):
            return []

        self.update_info()

        if self.mtime > target_time or self.children is None:
            self.update_children()

        for child in self.children:
            ret += child.flatlist(target_time, callstack + [self])

        return ret

    def update_info(self):
        self.mtime = self.storage.modified_time(self.name)

    def update_children(self):
        ret = []

        try:
            fh = self.storage.open(self.name, 'r')
            subfiles = self.parse_imports(fh)

            for subfile in subfiles:
                for path in self.searchpath:
                    candidate = "%s/%s/%s" % (self.basepath, path, subfile)

                    if self.storage.exists(candidate):
                        ret.append(get_by_name(self.__class__, self.storage, candidate, self.searchpath))
                        break
        except:
            pass

        self.children = ret

    def parse_imports(self, fh):
        raise NotImplementedError

class CssCompiler(SubProcessCompiler):
    tree_object = BaseFileTree

    def get_search_path(self):
        return ['.']

    def is_outdated(self, infile, outfile):
        tree = get_by_name(self.tree_object, self.storage, infile, self.get_search_path())
        target_time = self.storage.modified_time(outfile)

        for node in tree.flatlist(target_time):
            if node.mtime > target_time:
                return True

        return False

def get_by_name(actual_class, storage, name, searchpath = ['.']):
    path = normpath(name)

    if path in actual_class.files_info:
        return actual_class.files_info[path]
    else:
        return actual_class(storage, path, searchpath)
