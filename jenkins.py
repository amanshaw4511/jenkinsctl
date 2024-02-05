#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
from jbuild import handle_build_command
from api4jenkins import Jenkins
from config import settings


server_url = settings.server_url
username = settings.username
api_key = settings.api_key


def get_client():
    return Jenkins(server_url, auth=(username, api_key))

def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Subcommand", dest="subcommand")

    build_parser = subparsers.add_parser("build", help="run new build")
    build_parser.set_defaults(func=handle_build_command, client=get_client)
    build_parser.add_argument(
        "-f", "--file", type=argparse.FileType("r"), help="Yaml configuration file"
    )
    build_parser.add_argument("-v", "--verbose", action="store_true")
    build_parser.add_argument("-s", "--suppress-logs")
    build_parser.add_argument("--param", action="append", default=[])

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)


get_args()
