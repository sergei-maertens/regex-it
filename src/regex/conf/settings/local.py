import sys
import tempfile

if "test" in sys.argv:
    MEDIA_ROOT = tempfile.mkdtemp()
    PRIVATE_MEDIA_ROOT = tempfile.mkdtemp()
