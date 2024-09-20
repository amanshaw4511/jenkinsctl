from typing import Optional

from jenkinsctl.configs.session import Session
from jenkinsctl.jenkins.commons import get_last_build_no_if_none
from jenkinsctl.jenkins.job import progressive_log


def logs_handler(session: Session, job_name: str, build_no: Optional[int]):
    build_no = get_last_build_no_if_none(session, job_name, build_no)
    progressive_log(session, job_name, build_no)
