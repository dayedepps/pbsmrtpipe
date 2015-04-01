"""This needs to be completely redone to use the DI model"""
import logging
import pprint
import unittest
from collections import namedtuple

from nose.plugins.attrib import attr
import time

import pbsmrtpipe.driver as D
import pbsmrtpipe.bgraph as B
from pbsmrtpipe.decos import timeit
from pbsmrtpipe.pb_io import WorkflowLevelOptions
from base import HAS_CLUSTER_QSUB, SLOW_ATTR
import base as TB


log = logging.getLogger(__name__)


def _get_registered_tasks_and_operators():
    import pbsmrtpipe.loader as L
    return L.load_all_installed_pb_tasks(), L.load_all_installed_chunk_operators()


def _get_registered_files():
    from pbsmrtpipe.core import REGISTERED_FILE_TYPES
    return REGISTERED_FILE_TYPES


def _get_dev_task_bindings():
    b1 = [('$entry:e_01', 'pbsmrtpipe.tasks.dev_hello_world:0')]

    b2 = [('pbsmrtpipe.tasks.dev_hello_world:0', 'pbsmrtpipe.tasks.dev_hello_worlder:0'),
          ('pbsmrtpipe.tasks.dev_hello_world:0', 'pbsmrtpipe.tasks.dev_hello_garfield:0')]

    return b1 + b2


def _get_dist_dev_bindings():
    bs = _get_dev_task_bindings()

    b2 = [('pbsmrtpipe.tasks.dev_hello_world:0', 'pbsmrtpipe.tasks.dev_hello_distributed:0'),
          ('pbsmrtpipe.tasks.dev_hello_worlder:0', 'pbsmrtpipe.tasks.dev_hello_distributed:1')]

    return bs + b2


def _get_entry_points():
    return {'$entry:e_01': 'my_ep.txt'}


def _to_wopts(tmp_dir):
    return WorkflowLevelOptions(True, 24, 6, 18, 24, False, None, tmp_dir, None, True)


def _test_run_driver(chunk_operators, register_tasks_d, rfiles_d, ep_d, bg, job_output_dir, tmp_dir, task_opts, cluster_renderer):
    # TODO Add a timeout.

    log.debug("Entry points:")
    log.debug(pprint.pformat(ep_d, indent=4))
    log.debug(("output dir", job_output_dir))
    log.debug(("tmp dir", tmp_dir))

    workflow_level_options = WorkflowLevelOptions(True, 24, 6, 18, 24, False, None, tmp_dir, None, True)

    log.debug(workflow_level_options)

    started_at = time.time()

    state = D.exe_workflow(chunk_operators, ep_d, bg, task_opts, workflow_level_options,
                           job_output_dir, register_tasks_d, rfiles_d, cluster_renderer,
                           D.run_task_manifest, D.run_task_manifest_on_cluster)
    run_time = time.time() - started_at
    log.debug("Completed running driver test in {s:.2} sec".format(s=run_time))
    return state


JobConfig = namedtuple('JobConfig', 'job_name task_opts bindings_str ep_d cluster_renderer tmp_dir_func tmp_file_func')


@timeit
def _run_driver_from_job_config(job_config):
    """
    :type job_config: JobConfig
    :param job_config:
    :return:
    """
    job_output_dir = job_config.tmp_dir_func(job_config.job_name)
    tmp_dir = job_config.tmp_dir_func(job_config.job_name + '_tmp')

    ep_d = {e_id: job_config.tmp_file_func(file_name) for e_id, file_name in job_config.ep_d.iteritems()}

    rtasks, chunk_operators = _get_registered_tasks_and_operators()
    rfiles = _get_registered_files()
    bgraph_ = B.binding_strs_to_binding_graph(rtasks, job_config.bindings_str)

    state = _test_run_driver(chunk_operators, rtasks, rfiles, ep_d, bgraph_, job_output_dir, tmp_dir, job_config.task_opts, job_config.cluster_renderer)
    return state

@attr(SLOW_ATTR)
class LocalHelloDevTest(unittest.TestCase):
    JOB_CONFIG = JobConfig('job_dev_test', {},
                           _get_dev_task_bindings(),
                           _get_entry_points(),
                           None,
                           TB.get_temp_dir,
                           TB.get_temp_file)

    def test_run_driver(self):
        state = _run_driver_from_job_config(self.JOB_CONFIG)
        self.assertTrue(state, "Job {n} failed".format(n=self.JOB_CONFIG.job_name))

@attr(SLOW_ATTR)
@unittest.skipIf(not HAS_CLUSTER_QSUB, "No qsub exe found.")
class MyTest(unittest.TestCase):
    JOB_CONFIG = JobConfig('job_dev_dist_test', {},
                           _get_dev_task_bindings(),
                           _get_entry_points(),
                           None,
                           TB.get_temp_cluster_dir,
                           TB.get_temp_cluster_file)

    def test_run_driver(self):
        state = _run_driver_from_job_config(self.JOB_CONFIG)
        self.assertTrue(state, "Job {n} failed".format(n=self.JOB_CONFIG.job_name))