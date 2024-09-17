#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete
from .jbuild import handle_build_command, handle_list_command
from api4jenkins import Jenkins
from .config import settings
from .jget_config import handle_config_comand, handle_json_command, handle_logs_command, handle_rebuild_command


server_url = settings.server_url
username = settings.username
api_key = settings.api_key


def get_client():
    return Jenkins(server_url, auth=(username, api_key))


def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Subcommand", dest="subcommand")

    add_build_subparser(subparsers)
    add_get_config_subparser(subparsers)
    add_list_subparser(subparsers)
    add_logs_subparser(subparsers)
    add_json_subparser(subparsers)
    add_rebuild_subparser(subparsers)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)



def add_rebuild_subparser(subparsers):
    subparser = subparsers.add_parser("rebuild", help="print the logs of build")
    subparser.set_defaults(func=handle_rebuild_command, client=get_client)
    subparser.add_argument("job_name")
    subparser.add_argument("build_no", type=int, nargs="?")
    subparser.add_argument("-v", "--verbose", action="store_true")
 

def add_logs_subparser(subparsers):
    subparser = subparsers.add_parser("logs", help="print the logs of build")
    subparser.set_defaults(func=handle_logs_command, client=get_client)
    subparser.add_argument("job_name")
    subparser.add_argument("build_no", type=int, nargs="?")
    subparser.add_argument("-v", "--verbose", action="store_true")
 

def add_json_subparser(subparsers):
    subparser = subparsers.add_parser("json", help="print the api json of build")
    subparser.set_defaults(func=handle_json_command, client=get_client)
    subparser.add_argument("job_name")
    subparser.add_argument("build_no", type=int, nargs="?")
    subparser.add_argument("-v", "--verbose", action="store_true")
 

def add_list_subparser(subparsers):
    subparser = subparsers.add_parser("list", help="list all build")
    subparser.set_defaults(func=handle_list_command, client=get_client)
    subparser.add_argument("job_name")
    subparser.add_argument("-v", "--verbose", action="store_true")

def add_get_config_subparser(subparsers):
    subparser = subparsers.add_parser("config", help="get config of a build")
    subparser.set_defaults(func=handle_config_comand, client=get_client)
    subparser.add_argument("job_name")
    subparser.add_argument("build_no", type=int, nargs="?")
    subparser.add_argument("-v", "--verbose", action="store_true")

def add_build_subparser(subparsers):
    subparser = subparsers.add_parser("build", help="run new build")
    subparser.set_defaults(func=handle_build_command, client=get_client)
    subparser.add_argument(
        "-f", "--file", type=argparse.FileType("r"), help="Yaml configuration file"
    )
    subparser.add_argument("-v", "--verbose", action="store_true")
    subparser.add_argument("-s", "--suppress-logs", action="store_true")
    subparser.add_argument("--param", action="append", default=[])


if __name__ == '__main__':
    get_args()