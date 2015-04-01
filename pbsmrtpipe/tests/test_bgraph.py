import unittest
import logging

# this will load all the tasks modules

import pbsmrtpipe.loader
RTASKS = pbsmrtpipe.loader.load_all_installed_pb_tasks()

import pbsmrtpipe.bgraph as B
import pbsmrtpipe.cluster as C
import pbsmrtpipe.pb_io as IO

INSTALLED_CLUSTER_TEMPLATES = C.load_installed_cluster_templates()

log = logging.getLogger(__name__)

DEEP_DEBUG = True


def _to_workflow_options_settings(path):
    preset_record = IO.parse_pipeline_preset_xml(path)
    d = dict(preset_record.workflow_options)
    wopts = IO.WorkflowLevelOptions.from_id_dict(d)
    return wopts


class TestBindingFormat(unittest.TestCase):

    bs = ['pbsmrtpipe.tasks.dev_hello:1',
          'pbsmrtpipe.tasks.dev_hello2:9:1']

    results = [('pbsmrtpipe.tasks.dev_hello', 0, 1),
               ('pbsmrtpipe.tasks.dev_hello2', 9, 1)]

    def test_binding_format(self):
        for b in self.bs:
            self.assertTrue(B._validate_binding_format(b))

    def test_binding_str_format(self):
        for b, r in zip(self.bs, self.results):
            r2 = B.binding_str_to_task_id_and_instance_id(b)
            self.assertEquals(r, r2)


class TestConvertBindingStrToXml(unittest.TestCase):

    bs = [('entry:e_01', 'pbsmrtpipe.tasks.my_task:0'),
        ('entry:e_02', 'pbsmrtpipe.tasks.my_task2:0'),
        ('pbsmrtpipe.tasks.my_task:0', 'pbsmrtpipe.tasks.my_task2:1')]

    def test_to_xml(self):
        xml = B.binding_strs_to_xml(self.bs)
        log.info(str(xml))
        self.assertIsNotNone(xml)
