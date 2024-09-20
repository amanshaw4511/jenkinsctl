from jenkinsctl.jenkins.job import get_job
from jenkinsctl.jenkins.utils import get_last_build


def get_last_build_no_if_none(session, job_name, build_no):
    if build_no is None:
        job = get_job(session, job_name)
        return get_last_build(job)
    return build_no
