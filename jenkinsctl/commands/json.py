from typing import Optional

from jenkinsctl.configs.session import Session
from jenkinsctl.jenkins.commons import get_last_build_no_if_none
from jenkinsctl.jenkins.console_util import print_json
from jenkinsctl.jenkins.job import progressive_log, get_build
from jenkinsctl.jenkins.utils import normalize_job_path


def json_handler(session: Session, job_name: str, build_no: Optional[int]):
    job_name = normalize_job_path(job_name)
    build_no = get_last_build_no_if_none(session, job_name, build_no)
    build = get_build(session, job_name, build_no)
    print_json(build)