# -*- coding: utf-8 flake8: noqa -*-
import os
import sys


if sys.platform.startswith('win'):
    os.environ.setdefault('NUMBER_OF_PROCESSORS', '1')


from .test_collector import *
from .test_compiler import *
from .test_compressor import *
from .test_template import *
from .test_glob import *
from .test_middleware import *
from .test_packager import *
from .test_storage import *
from .test_utils import *
from .test_views import *
