import time

from urllib.parse import urlparse

from jenkinsctl.configs.session import Session

def _remove_base_url(url: str):
    return urlparse(url).path

def _get(session: Session, url: str):
    url = _remove_base_url(url)
    url = f"{url}api/json"
    return session.get(url).json()


def build_job(session: Session, job_name: str, params: dict):
    response = None
    if len(params) == 0:
        url = f"/job/{job_name}/build"
        response = session.post(url)
    else:
        url = f"/job/{job_name}/buildWithParameters"
        response = session.post(url, params=params)

    return response.headers.get("Location")


def get_job(session: Session, job_name: str):
    url = f"/job/{job_name}/"
    return _get(session, url)


def get_jobs(session: Session, folder_name: str):
    if folder_name.strip() == "":
        return _get(session, "")

    url = f"/job/{folder_name}/"
    return _get(session, url)


def get_builds_iter(session: Session, job_json):
    builds = job_json["builds"]
    for build in builds:
        yield _get_build(session, job_json, build["number"])


def _get_build(session: Session, job_json, build_no):
    builds = job_json["builds"]
    build = next((build for build in builds if build["number"] == build_no), None)

    return _get(session, build["url"])


def get_build(session: Session, job_name: str, build_no: int):
    url = f"/job/{job_name}/{build_no}/"
    return _get(session, url)


def progressive_log(session: Session, job_name: str, build_no: int):
    url = f"/job/{job_name}/{build_no}/logText/progressiveText"
    start_byte = 0
    while True:
        response = session.get(url, params={'start': start_byte})
        text = response.text
        print(text, end="")
        start_byte = int(response.headers.get('X-Text-Size', 0))
        if response.headers.get('X-More-Data') == 'false' or text.strip() == "":
            break
        time.sleep(2)
