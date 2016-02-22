#!/usr/bin/env python
"""
A cross-platform compatible `npm install` call, checking whether npm is
in fact installed on the system first (and on windows, checking that the
npm version is at least 3.0 because of a bug in 2.x with MAX_PATH)
"""
import distutils.spawn
import os
from pkg_resources import parse_version
import re
import subprocess
import sys


def main():
    tests_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    if os.name == 'nt':
        try:
            npm_paths = subprocess.check_output(['where', 'npm.cmd'])
        except subprocess.CalledProcessError:
            return
        else:
            npm_bin = re.split(r'\r?\n', npm_paths)[0]
    else:
        npm_bin = distutils.spawn.find_executable('npm')
    if not npm_bin:
        return
    if os.name == 'nt':
        os.environ.setdefault('APPDATA', '.')
        npm_version = subprocess.check_output([npm_bin, '--version']).strip()
        # Skip on windows if npm version is less than 3 because of
        # MAX_PATH issues in version 2
        if parse_version(npm_version) < parse_version('3.0'):
            return
    pipe = subprocess.Popen([npm_bin, 'install'],
        cwd=tests_dir, stdout=sys.stdout, stderr=sys.stderr)
    pipe.communicate()
    sys.exit(pipe.returncode)


if __name__ == '__main__':
    main()
