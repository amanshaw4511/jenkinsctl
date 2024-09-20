import requests

from jenkinsctl.config import settings
from jenkinsctl.jenkins.job import get_job, get_builds_iter, get_build, build_job, progressive_log
import json

from jenkinsctl.jenkins.utils import print_build, get_build_params

server_url = settings.server_url
username = settings.username
api_key = settings.api_key


def _get_session():
    session = requests.Session()
    session.auth = (username, api_key)
    return session

def client_log(job_name: str, build_no: int):
    session = _get_session()
    progressive_log(session, server_url, job_name, build_no)
    session.close()


def client_get_job(job_name: str):
    session = _get_session()
    job = get_job(session, server_url, job_name)
    print(json.dumps(job))
    session.close()


def client_list(job_name: str):
    session = _get_session()
    for build in get_builds_iter(session, get_job(session, server_url, job_name)):
        print_build(build)
    session.close()


def client_build(job_name: str, params: dict):
    session = _get_session()
    build_job(session, server_url, job_name, params)
    session.close()


def client_rebuild(job_name: str, build_no: int):
    session = _get_session()
    build_json = get_build(session, server_url, job_name, build_no)
    build_job(session, server_url, job_name, get_build_params(build_json))
    session.close()
