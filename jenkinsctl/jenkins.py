#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete
from .jbuild import handle_build_command
from api4jenkins import Jenkins
from .config import settings
from .jget_config import handle_get_config


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

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)


def add_build_subparser(subparsers):
    subparser = subparsers.add_parser("build", help="run new build")
    subparser.set_defaults(func=handle_build_command, client=get_client)
    subparser.add_argument(
        "-f", "--file", type=argparse.FileType("r"), help="Yaml configuration file"
    )
    subparser.add_argument("-v", "--verbose", action="store_true")
    subparser.add_argument("-s", "--suppress-logs")
    subparser.add_argument("--param", action="append", default=[])


def add_get_config_subparser(subparsers):
    subparser = subparsers.add_parser("config", help="get config of a build")
    subparser.set_defaults(func=handle_get_config, client=get_client)
    subparser.add_argument("job_name")
    subparser.add_argument("build_no", type=int)


if __name__ == '__main__':
    get_args()
