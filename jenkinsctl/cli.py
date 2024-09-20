import logging
from io import TextIOWrapper
from typing import Optional

import click
from api4jenkins import Jenkins

from jenkinsctl.commands.build import build_handler
from jenkinsctl.commands.config import config_handler
from jenkinsctl.commands.json import json_handler
from jenkinsctl.commands.list import list_handler
from jenkinsctl.commands.logs import logs_handler
from jenkinsctl.commands.rebuild import rebuild_handler
from jenkinsctl.configs.config import settings
from jenkinsctl.configs.logging_config import setup_logging
from jenkinsctl.configs.session import Session

server_url: str = settings.server_url
username: str = settings.username
api_key: str = settings.api_key


def _get_session():
    session = Session(server_url)
    session.auth = (username, api_key)
    return session


def get_client() -> Jenkins:
    """Initialize and return a Jenkins client."""
    return Jenkins(server_url, auth=(username, api_key))


@click.group()
@click.option('-v', '--verbose', is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """A command-line tool to interact with Jenkins jobs"""
    log_level: int = logging.DEBUG if verbose else logging.INFO
    logger = setup_logging(log_level)

    logger.info(f"Starting Jenkins CLI")


@cli.command("list")
@click.argument("job_name")
def list_command(job_name: str) -> None:
    """List all builds of a Jenkins job"""
    with _get_session() as session:
        list_handler(session, job_name)


@cli.command("logs")
@click.argument("job_name")
@click.argument("build_no", required=False, type=int)
def logs_command(job_name: str, build_no: Optional[int]) -> None:
    """Print logs of a Jenkins build"""
    with _get_session() as session:
        logs_handler(session, job_name, build_no)


@cli.command("json")
@click.argument("job_name")
@click.argument("build_no", required=False, type=int)
def json_command(job_name: str, build_no: Optional[int]) -> None:
    """Fetch and print the JSON API response of a Jenkins build"""
    with _get_session() as session:
        json_handler(session, job_name, build_no)


@cli.command("config")
@click.argument("job_name")
@click.argument("build_no", required=False, type=int)
def config_command(job_name: str, build_no: Optional[int]) -> None:
    """Get the configuration of a specific build in YAML format"""
    with _get_session() as session:
        config_handler(session, job_name, build_no)


@cli.command("rebuild")
@click.argument("job_name")
@click.argument("build_no", required=False, type=int)
def rebuild_command(job_name: str, build_no: Optional[int]) -> None:
    """Rebuild a specific Jenkins job"""
    with _get_session() as session:
        rebuild_handler(session, job_name, build_no)


@cli.command("build")
@click.option("-p", "--param", multiple=True,
              help="Override parameters in the YAML configuration (e.g., --param key=value)")
@click.option("-f", "--file", type=click.File('r'), required=True, help="YAML configuration file for the Jenkins job")
def build_command(file: TextIOWrapper, param: tuple[str]) -> None:
    """Trigger a new Jenkins build"""
    params = [p for p in param]
    with _get_session() as session:
        build_handler(session, file, params)


# Entry point
if __name__ == '__main__':
    cli()
