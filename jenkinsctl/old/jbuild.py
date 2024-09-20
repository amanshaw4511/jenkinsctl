#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import sys
from datetime import datetime
from itertools import islice

import yaml
from dateutil import tz
from rich.console import Console
from rich.table import Table


def format_timestamp(epoch_timestamp):
    # Convert epoch timestamp to a naive datetime object
    naive_dt = datetime.fromtimestamp(epoch_timestamp / 1000)

    # Get the local timezone
    local_tz = tz.tzlocal()

    # Convert naive datetime to local timezone
    local_dt = naive_dt.astimezone(local_tz)

    # Format the datetime object to a string
    return local_dt.strftime('%Y-%m-%d %H:%M')


def handle_list_command(client, job_name):
    job = client.get_job(job_name)

    console = Console()
    table = Table(show_header=True, header_style="bold cyan", box=None)

    table.add_column("NUMBER", width=6)
    table.add_column("IN PROGRESS", width=15)
    table.add_column("RESULT", width=10)
    table.add_column("BUILDING", width=8)
    table.add_column("BRANCH", width=15)
    table.add_column("REVISION", width=8)
    table.add_column("STARTED BY", width=15)
    table.add_column("BUILD TIME", width=20)

    for build in islice(job.iter(), 5):
        api_json = build.api_json()
        actions = api_json["actions"]

        cause = None
        branch = None
        revision = None
        for action in actions:
            if action.get("causes") is not None and len(action["causes"]) > 0:
                cause = action["causes"][0]["userId"]

            if action.get("lastBuiltRevision"):
                branch_prefix = "refs/remotes/origin/"
                branch = action["lastBuiltRevision"]["branch"][0]["name"]
                if branch.startswith(branch_prefix):
                    branch = branch[len(branch_prefix):]
                revision = action["lastBuiltRevision"]["SHA1"][:5]

        table.add_row(str(build.number),
                      str(api_json.get("in_progress")),
                      str(api_json.get("result")),
                      str(api_json.get("building")),
                      branch,
                      revision,
                      cause,
                      str(format_timestamp(api_json.get("timestamp"))))

    console.print(table)


def handle_build_command(client, file, param):
    conf = get_conf(file, param)

    create_build(client, conf)


def get_config_from_yaml(file):
    config_data = None
    try:
        with open(file.name, "r") as config_file:
            config_data = yaml.safe_load(config_file)  # Use safe_load for YAML
    except FileNotFoundError:
        print(f"Error: Configuration file '{file}' not found.")
        sys.exit()
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in '{file}': {e}")
        sys.exit()

    return config_data


def get_conf(file, params):
    config = get_config_from_yaml(file)
    override_params(params, config)
    return config


def override_params(params, file_config):
    for param in params:
        name, value = param.split('=')
        file_config['params'][name] = value


def create_build(client, conf, vprint=print):
    vprint(f"client version: {client.version}")

    queued_item = client.build_job(conf["job"], **conf["params"])
    vprint(f"queued : {queued_item}")
