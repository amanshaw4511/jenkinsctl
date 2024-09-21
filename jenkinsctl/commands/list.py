from itertools import islice

from rich.console import Console
from rich.table import Table

from jenkinsctl.configs.session import Session
from jenkinsctl.jenkins.console_util import format_timestamp
from jenkinsctl.jenkins.job import get_job, get_builds_iter
from jenkinsctl.jenkins.utils import normalize_job_path


def list_handler(session: Session, job_name: str, number: int):
    job_name = normalize_job_path(job_name)
    job = get_job(session, job_name)

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

    for build in islice(get_builds_iter(session, job), number):
        number = build["number"]
        building = build["building"]
        in_progress = build["inProgress"]
        result = build["result"]
        timestamp = build["timestamp"]

        actions = build["actions"]
        causes = next((action["causes"] for action in actions if action.get("causes") is not None), None)
        user_id = next((cause["userId"] for cause in causes if cause.get("userId") is not None), None)

        branch = None
        revision = None
        # fixme: not working below code
        # last_build = next((action["lastBuildRevision"] for action in actions if action.get("lastBuildRevision") is not None))
        last_build = None
        if last_build:
            branch_prefix = "refs/remotes/origin/"
            branch = last_build["branch"][0]["name"]
            if branch.startswith(branch_prefix):
                branch = branch[len(branch_prefix):]
            revision = last_build["SHA1"][:5]


        table.add_row(
            str(number),
            str(in_progress),
            str(result),
            str(building),
            branch,
            revision,
            user_id,
            str(format_timestamp(timestamp)))

    console.print(table)
