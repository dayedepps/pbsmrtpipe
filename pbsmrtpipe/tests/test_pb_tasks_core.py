import os
import unittest
import logging

from pbsmrtpipe.constants import to_file_ns
import pbsmrtpipe.core
from pbsmrtpipe.models import FileType, FileTypes, RunnableTask
import pbsmrtpipe.loader as L


REGISTERED_TASKS = pbsmrtpipe.loader.load_all_installed_pb_tasks()
REGISTERED_FILES = pbsmrtpipe.loader.load_all_registered_file_types()

from base import TEST_DATA_DIR

log = logging.getLogger(__name__)


class TestLoading(unittest.TestCase):

    def test_loading_di_tasks(self):
        log.info(REGISTERED_TASKS)
        log.info(pbsmrtpipe.core.REGISTERED_FILE_TYPES)
        self.assertTrue(True)

    def test_task_manifest_serialization(self):
        path = os.path.join(TEST_DATA_DIR, 'task-manifest.json')
        r = RunnableTask.from_manifest_json(path)
        self.assertIsInstance(r, RunnableTask)

    def test_file_type_eq(self):
        f = FileType(to_file_ns('fasta'), "file", "fasta", 'text/plain')
        self.assertEqual(id(f), id(FileTypes.FASTA))


