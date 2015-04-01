import unittest
import logging
import pprint

log = logging.getLogger(__name__)


class TestLoadingOperators(unittest.TestCase):
    def test_loading(self):
        import pbsmrtpipe.loader as L
        operators = L.load_all_installed_chunk_operators()
        emsg = "Unable to load operators"
        log.debug(pprint.pformat(operators, indent=4))
        self.assertTrue(len(operators) > 0, emsg)
