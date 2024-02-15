#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import time
import sys
import yaml
from threading import Thread

from .commons import use_vprint


def handle_build_command(args):
    vprint = use_vprint(args.verbose)
    vprint(f"Passed args : {vars(args)}")

    conf = get_conf(args, vprint)
    vprint("Final config: ", conf)

    create_build(args.client, conf, args.suppress_logs, vprint)


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


def get_build(queued_item):
    build = queued_item.get_build()
    while build == None:
        time.sleep(2)
        build = queued_item.get_build()
    return build


def get_build_no(queued_item):
    return queued_item.api_json()["executable"]["number"]


def print_build_log(build):
    for line in build.progressive_output():
        print(line)


def approve_pending_input(build):
    if not hasattr(build, 'get_pending_input'):
        return

    while not build.get_pending_input() and build.building:
        time.sleep(1)

    if build.building:
        build.get_pending_input().submit()


def create_build(client, conf, suppress_logs: bool, vprint=print):

    client = client()
    vprint(f"client version: {client.version}")

    job = client.get_job(conf["job"])
    vprint(f"job : {job}")

    queued_item = job.build(**conf["params"])
    vprint(f"queued : {queued_item}")

    build = get_build(queued_item)
    vprint(f"build : {build}")

    build_number = get_build_no(queued_item)

    if not suppress_logs:
        print(f"STARTED... build number : {build_number}")

    approve_pending_input_thread = Thread(
        target=approve_pending_input, args=(build,))
    approve_pending_input_thread.start()

    if not suppress_logs:
        log_thread = Thread(target=print_build_log, args=(build,))
        log_thread.start()
        log_thread.join()

    approve_pending_input_thread.join()

    if not suppress_logs:
        print(f"FINISHED... build number : {build_number}")
    else:
        print(build_number)

    return build_number
