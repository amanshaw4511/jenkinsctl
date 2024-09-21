from typing import Optional

from jenkinsctl.configs.session import Session
from jenkinsctl.jenkins.commons import get_last_build_no_if_none
from jenkinsctl.jenkins.job import get_build
from jenkinsctl.jenkins.utils import get_build_params, to_yaml, normalize_job_path


def config_handler(session: Session, job_name: str, build_no: Optional[int]):
    job_name = normalize_job_path(job_name)
    build_no = get_last_build_no_if_none(session, job_name, build_no)

    build = get_build(session, job_name, build_no)
    params = get_build_params(build)
    print(to_yaml(job_name, params))
