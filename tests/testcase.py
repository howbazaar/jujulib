import shutil
import tempfile
import unittest


class TestCase(unittest.TestCase):
    """A useful base testcase with extra methods."""

    def mkdir(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        return d
