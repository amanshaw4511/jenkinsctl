#!/usr/bin/env python3

import logging
from typing import Optional, List

import click
from api4jenkins import Jenkins

from jenkinsctl.jenkins.client import client_list
from .config import settings
from .jbuild import handle_build_command, handle_list_command
from .jget_config import handle_config_comand, handle_json_command, handle_logs_command, handle_rebuild_command


server_url: str = settings.server_url
username: str = settings.username
api_key: str = settings.api_key

logger = logging.getLogger(__name__)


def get_client() -> Jenkins:
    """Initialize and return a Jenkins client."""
    return Jenkins(server_url, auth=(username, api_key))


@click.group()
@click.option('-v', '--verbose', is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """A command-line tool to interact with Jenkins jobs"""
    log_level: int = logging.DEBUG if verbose else logging.INFO


@cli.command()
@click.argument("job_name")
def list(job_name: str) -> None:
    """List all builds of a Jenkins job"""
    handle_list_command(get_client(), job_name)


@cli.command()
@click.argument("job_name")
@click.argument("build_no", required=False, type=int)
def logs(job_name: str, build_no: Optional[int]) -> None:
    """Print logs of a Jenkins build"""
    handle_logs_command(get_client(), job_name, build_no)


@cli.command()
@click.argument("job_name")
@click.argument("build_no", required=False, type=int)
def json(job_name: str, build_no: Optional[int]) -> None:
    """Fetch and print the JSON API response of a Jenkins build"""
    handle_json_command(get_client(), job_name, build_no)


@cli.command()
@click.argument("job_name")
@click.argument("build_no", required=False, type=int)
def config(job_name: str, build_no: Optional[int]) -> None:
    """Get the configuration of a specific build in YAML format"""
    handle_config_comand(get_client(), job_name, build_no)


@cli.command()
@click.argument("job_name")
@click.argument("build_no", required=False, type=int)
def rebuild(job_name: str, build_no: Optional[int]) -> None:
    """Rebuild a specific Jenkins job"""
    handle_rebuild_command(get_client(), job_name, build_no)


@cli.command()
@click.option("-p", "--param", multiple=True, help="Override parameters in the YAML configuration (e.g., --param key=value)")
@click.option("-f", "--file", type=click.File('r'), required=True, help="YAML configuration file for the Jenkins job")
def build( file: click.File, param: Optional[List[str]]) -> None:
    """Trigger a new Jenkins build"""
    handle_build_command(get_client(), file, param)


@cli.command()
def test() -> None:
    """Test command for Jenkins job"""
    job_name = "TestParam"
    client_list(job_name)


# Entry point
if __name__ == '__main__':
    cli()
