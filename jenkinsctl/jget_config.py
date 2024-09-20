import json
import logging

import yaml
from rich.console import Console

from .commons import use_vprint

logger = logging.getLogger(__name__)


def handle_rebuild_command(client, job_name, build_no):
    build = get_build(client, job_name, build_no)
    params = get_params(build)
    client.build_job(job_name, **params)


def handle_json_command(client, job_name, build_no):
    build = get_build(client, job_name, build_no)

    out = build.api_json()
    out["actions"] = [action for action in out["actions"]]
    out_str = json.dumps(out)
    Console().print_json(out_str)


def handle_logs_command(client, job_name, build_no):
    build = get_build(client, job_name, build_no)

    for line in build.progressive_output():
        print(line)


def handle_config_comand(client, job_name, build_no):
    build = get_build(client, job_name, build_no)

    params = get_params(build)

    print(to_yaml(job_name, params))


def get_build(client, job_name, build_no):
    job = client.get_job(job_name)

    final_build_no = get_last_build_no(job) if build_no is None else build_no

    build = job.get(final_build_no)

    return build


def get_last_build_no(job):
    return job.get_last_build().number


def get_params(build):
    return dict([(param.name, param.value) for param in build.get_parameters()])


def to_yaml(job_name, params):
    return yaml.dump({"job": job_name, "params": params})
