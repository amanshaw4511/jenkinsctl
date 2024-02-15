import yaml

from .commons import use_vprint


def handle_get_config(args):
    vprint = use_vprint(args.verbose)
    vprint(f"Passed args : {vars(args)}")

    client = args.client()

    job_name = args.job_name

    build = get_build(client, vprint, job_name, args.build_no)

    params = get_params(build)

    print(to_yaml(job_name, params))


def get_build(client, vprint, job_name, build_no):
    job = client.get_job(job_name)

    final_build_no = get_last_build_no(job) if build_no is None else build_no
    vprint(f"final build no {final_build_no}")

    build = job.get(final_build_no)

    return build


def get_last_build_no(job):
    return job.get_last_build().number


def get_params(build):
    return dict([(param.name, param.value) for param in build.get_parameters()])


def to_yaml(job_name, params):
    return yaml.dump({"job": job_name, "params": params})
