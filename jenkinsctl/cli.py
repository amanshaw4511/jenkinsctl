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
    parser = argparse.ArgumentParser(
        description="A command-line tool to interact with Jenkins jobs",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(
        title="Subcommands",
        description="Available commands to interact with Jenkins",
        help="Choose one of the following subcommands",
        dest="subcommand",
    )

    add_build_subparser(subparsers)
    add_get_config_subparser(subparsers)
    add_list_subparser(subparsers)
    add_logs_subparser(subparsers)
    add_json_subparser(subparsers)
    add_rebuild_subparser(subparsers)

    argcomplete.autocomplete(parser)

    # Parse arguments and handle missing subcommands
    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        parser.exit()

    args.func(args)


def add_job_name_argument(subparser):
    subparser.add_argument("job_name", help="Name of the Jenkins job")


def add_build_no_argument(subparser):
    subparser.add_argument("build_no", type=int, nargs="?", help="Build number (optional, defaults to last build)")


def add_verbose_argument(subparser):
    subparser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")


def add_rebuild_subparser(subparsers):
    subparser = subparsers.add_parser("rebuild", help="Rebuild a specific Jenkins job")
    subparser.set_defaults(func=handle_rebuild_command, client=get_client)
    add_job_name_argument(subparser)
    add_build_no_argument(subparser)
    add_verbose_argument(subparser)


def add_logs_subparser(subparsers):
    subparser = subparsers.add_parser("logs", help="Print logs of a Jenkins build")
    subparser.set_defaults(func=handle_logs_command, client=get_client)
    add_job_name_argument(subparser)
    add_build_no_argument(subparser)
    add_verbose_argument(subparser)


def add_json_subparser(subparsers):
    subparser = subparsers.add_parser("json", help="Fetch and print the JSON API response of a Jenkins build")
    subparser.set_defaults(func=handle_json_command, client=get_client)
    add_job_name_argument(subparser)
    add_build_no_argument(subparser)
    add_verbose_argument(subparser)


def add_list_subparser(subparsers):
    subparser = subparsers.add_parser("list", help="List all builds of a Jenkins job")
    subparser.set_defaults(func=handle_list_command, client=get_client)
    add_job_name_argument(subparser)
    add_verbose_argument(subparser)


def add_get_config_subparser(subparsers):
    subparser = subparsers.add_parser("config", help="Get the configuration of a specific build in YAML format")
    subparser.set_defaults(func=handle_config_comand, client=get_client)
    add_job_name_argument(subparser)
    add_build_no_argument(subparser)
    add_verbose_argument(subparser)


def add_build_subparser(subparsers):
    subparser = subparsers.add_parser("build", help="Trigger a new Jenkins build")
    subparser.set_defaults(func=handle_build_command, client=get_client)
    subparser.add_argument(
        "-f", "--file", type=argparse.FileType("r"), required=True, help="YAML configuration file for the Jenkins job"
    )
    add_verbose_argument(subparser)
    subparser.add_argument("-p", "--param", action="append", default=[], help="Override parameters in the YAML configuration (e.g., --param key=value)")


if __name__ == '__main__':
    get_args()
