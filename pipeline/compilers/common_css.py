import re

from os.path import dirname, normpath
from datetime import datetime
from pipeline.compilers import SubProcessCompiler


class BaseFileTree(object):
    """
    The BaseFileTree represents a node and its children in a tree of @imported
    CSS files. It handles the parsing of them, in order to be able to check
    the modification date of the node itself and all its children.
    """
    files_info = {}
    import_exp = re.compile('@import\\s+("((?:[^"\r\n]|\\.)*)"|\'((?:[^\'\r\n]'
                            + '|\\.)*)\'|`((?:[^`]|\\.)*)`)')
    import_css = False
    extensions = ('.css',)

    def __init__(self, storage, name, searchpath=None):
        if searchpath is None:
            searchpath = ['.']

        self.storage = storage
        self.name = normpath(name)
        self.searchpath = searchpath
        self.mtime = datetime.fromtimestamp(0.0)
        self.children = None
        self.basepath = dirname(self.name)

        self.files_info[self.name] = self

    def flatlist(self, target_time, callstack=None):
        """
        Will return a flat up-to-date list containing the complete list of
        files that might be included by the current node, plus the current node
        itself.

        The information about those files is cached into memory in order to
        avoid a complete parse at every call.
        """

        if callstack is None:
            callstack = []

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
        """
        Updates the current node's modification date.
        """
        self.mtime = self.storage.modified_time(self.name)

    def update_children(self):
        """
        Triggers a re-population of the children list, by calling a parse of
        the file and then processing the result.
        """
        ret = []

        try:
            fhdl = self.storage.open(self.name, 'r')
            subfiles = self.parse_imports(fhdl)

            for subfile in subfiles:
                for path in self.searchpath:
                    candidate = "%s/%s/%s" % (self.basepath, path, subfile)

                    if self.storage.exists(candidate):
                        ret.append(get_by_name(
                            self.__class__,
                            self.storage,
                            candidate,
                            self.searchpath
                        ))
                        break
        except IOError:
            pass

        self.children = ret

    def parse_imports(self, fhdl):
        """
        Parses a file looking for @import directives.
        """
        ret = []

        for line in fhdl.readlines():
            matches = self.import_exp.findall(line)

            for match in matches:
                filename = ""

                if match[0][0] == '"':
                    filename = match[1]
                elif match[0][0] == "'":
                    filename = match[2]
                elif match[0][0] == "`":
                    filename = match[3]

                if filename == '':
                    continue

                if self.import_css or not filename.endswith(".css"):
                    found_ext = False
                    possible = []

                    for ext in self.extensions:
                        possible.append("%s%s" % (filename, ext))

                        if filename.endswith(ext):
                            found_ext = True
                            break

                    if found_ext:
                        ret.append(filename)
                    else:
                        ret += possible

        return ret


class CssCompiler(SubProcessCompiler):
    """
    The CSS Compiler class helps to write CSS-derived file compiler by handling
    the most common tasks that are almost identical for all the compilers.
    """
    tree_object = BaseFileTree
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith(self.tree_object.extensions)

    @staticmethod
    def get_search_path():
        """
        Returns the search path for this compiler. The @imported files will be
        looked for in this search path.
        """
        return ['.']

    def is_outdated(self, infile, outfile):
        tree = get_by_name(
            self.tree_object,
            self.storage,
            infile,
            self.get_search_path()
        )
        target_time = self.storage.modified_time(outfile)

        for node in tree.flatlist(target_time):
            if node.mtime > target_time:
                return True

        return False


def get_by_name(actual_class, storage, name, searchpath=None):
    """
    Returns a file node of the matching name. If the node does not exist, it is
    created on the fly.
    """

    if searchpath is None:
        searchpath = ['.']

    path = normpath(name)

    if path in actual_class.files_info:
        return actual_class.files_info[path]
    else:
        return actual_class(storage, path, searchpath)
