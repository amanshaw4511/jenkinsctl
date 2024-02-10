import yaml

def handle_get_config(args):
    # print(args)
    client = args.client()
    job_name = args.job_name

    job = client.get_job(job_name)
    build = job.get(int(args.build_no))
    params = get_params(build)
    print(to_yaml(job_name, params))


def get_params(build):
    return dict([ (param.name, param.value) for param in build.get_parameters() ])

def to_yaml(job_name, params):
    return yaml.dump( { "job" : job_name, "params": params})

