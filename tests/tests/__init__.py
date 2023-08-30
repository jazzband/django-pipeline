import os
import sys

if sys.platform.startswith("win"):
    os.environ.setdefault("NUMBER_OF_PROCESSORS", "1")


from .test_collector import *  # noqa
from .test_compiler import *  # noqa
from .test_compressor import *  # noqa
from .test_glob import *  # noqa
from .test_middleware import *  # noqa
from .test_packager import *  # noqa
from .test_storage import *  # noqa
from .test_template import *  # noqa
from .test_utils import *  # noqa
from .test_views import *  # noqa
