#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import sys
from datetime import datetime
from itertools import islice

import yaml
from api4jenkins import Jenkins
from dateutil import tz
from rich.console import Console
from rich.table import Table

from .commons import use_vprint


def format_timestamp(epoch_timestamp):
    # Convert epoch timestamp to a naive datetime object
    naive_dt = datetime.fromtimestamp(epoch_timestamp / 1000)

    # Get the local timezone
    local_tz = tz.tzlocal()

    # Convert naive datetime to local timezone
    local_dt = naive_dt.astimezone(local_tz)

    # Format the datetime object to a string
    return local_dt.strftime('%Y-%m-%d %H:%M')


def handle_list_command(args):
    client: Jenkins = args.client()
    job = args.job_name
    job = client.get_job(job)

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

    for build in islice(job.iter_all_builds(), 5):
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
                      str(build.in_progress),
                      str(build.result),
                      str(build.building),
                      branch,
                      revision,
                      cause,
                      str(format_timestamp(build.timestamp)))

    console.print(table)


def handle_build_command(args):
    vprint = use_vprint(args.verbose)
    vprint(f"Passed args : {vars(args)}")

    conf = get_conf(args, vprint)
    vprint("Final config: ", conf)

    create_build(args.client, conf, vprint)


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


def get_conf(args, vprint):
    config = get_config_from_yaml(args.file)
    vprint(f"Config from file : {config}")
    override_params(args, config)
    return config


def override_params(args, file_config):
    for param in args.param:
        name, value = param.split('=')
        file_config['params'][name] = value


def create_build(client, conf, vprint=print):
    client = client()
    vprint(f"client version: {client.version}")

    queued_item = client.build_job(conf["job"], **conf["params"])
    vprint(f"queued : {queued_item}")
