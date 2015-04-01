import logging

from pbsmrtpipe.schema_opt_utils import to_opt_id


log = logging.getLogger(__name__)

_FILTER_OPTS_NAMES = 'filter_trim filter_artifact_score use_subreads ' \
                     'filter_read_score filter_min_read_length ' \
                     'filter_max_read_length filter_min_subread_length ' \
                     'filter_max_subread_length ' \
                     'filter_whitelist filter_min_snr'.split()

_FILTER_OPTS = [to_opt_id(s) for s in _FILTER_OPTS_NAMES]
