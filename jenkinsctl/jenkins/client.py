import requests

from jenkinsctl.config import settings
from jenkinsctl.jenkins.job import get_job, get_builds_iter, get_build, build_job, progressive_log
import json

server_url = settings.server_url
username = settings.username
api_key = settings.api_key


def get_session():
    session = requests.Session()
    session.auth = (username, api_key)
    return session

def client_log(job_name: str, build_no: int):
    session = get_session()
    progressive_log(session, server_url, job_name, build_no)
    session.close()


def client_get_job(job_name: str):
    session = get_session()
    job = get_job(session, server_url, job_name)
    print(json.dumps(job))
    session.close()


def client_list(job_name: str):
    session = get_session()
    for build in get_builds_iter(session, get_job(session, server_url, job_name)):
        _print_build(build)
    session.close()


def client_build(job_name: str, params: dict):
    session = get_session()
    build_job(session, server_url, job_name, params)
    session.close()


def client_rebuild(job_name: str, build_no: int):
    session = get_session()
    build_json = get_build(session, server_url, job_name, build_no)
    build_job(session, server_url, job_name, _get_build_params(build_json))
    session.close()


def _get_build_params(build_json):
    actions = build_json["actions"]
    params = next((action["parameters"] for action in actions if action._get("parameters") is not None), None)
    params = dict([(param["name"], param["value"]) for param in params])
    return params


def _print_build(build_json):
    number = build_json["number"]
    building = build_json["building"]
    in_progress = build_json["inProgress"]
    result = build_json["result"]
    timestamp = build_json["timestamp"]

    actions = build_json["actions"]
    causes = next((action["causes"] for action in actions if action._get("causes") is not None), None)
    user_id = next((cause["userId"] for cause in causes if cause._get("userId") is not None), None)

    print(number, building, in_progress, result, timestamp, user_id)
    print(_get_build_params(build_json))
