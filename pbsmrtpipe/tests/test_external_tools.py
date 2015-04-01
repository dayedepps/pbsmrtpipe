import os
import logging
import unittest
import tempfile

import pbsmrtpipe.external_tools

from base import TEST_DATA_DIR

log = logging.getLogger(__name__)


def _to_tempfile(suffix):
    t = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    t.close()
    return t.name


class TestExternalTools(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.name = "nx_workflow.dot"
        cls.file_name = os.path.join(TEST_DATA_DIR, cls.name)

    @unittest.skip
    def test_convert_dot_to_png(self):
        output_png = _to_tempfile('_dot.png')

        status = pbsmrtpipe.external_tools.dot_file_to_png(self.file_name, output_png)
        self.assertTrue(status)

    def test_convert_dot_to_svg(self):
        output_svg = _to_tempfile("_dot.svg")
        status = pbsmrtpipe.external_tools.dot_file_to_png(self.file_name, output_svg)
        self.assertTrue(status)
