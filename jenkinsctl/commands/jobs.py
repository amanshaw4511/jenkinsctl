from jenkinsctl.configs.session import Session
from jenkinsctl.jenkins.job import get_jobs
from jenkinsctl.jenkins.utils import normalize_job_path


def jobs_handler(session: Session, folder_name: str):
    folder_name = normalize_job_path(folder_name)
    response = get_jobs(session, folder_name)
    all_jobs = response["jobs"]

    folders = [job for job in all_jobs if job["_class"] == "com.cloudbees.hudson.plugins.folder.Folder"]
    jobs = [job for job in all_jobs if job["_class"] != "com.cloudbees.hudson.plugins.folder.Folder"]

    for folder in folders:
        folder_name = folder["name"]
        print(f"[{folder_name}]")

    for job in jobs:
        job_name = job["name"]
        print(f"{job_name}")
