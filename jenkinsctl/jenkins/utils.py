import yaml


def get_build_params(build_json):
    actions = build_json["actions"]
    params = next((action["parameters"] for action in actions if action.get("parameters") is not None), [])
    params = dict([(param["name"], param["value"]) for param in params])
    return params


def normalize_job_path(path: str):
    return (path.strip()
            .removeprefix("/")
            .replace("/", "/job/"))


def print_build(build_json):
    number = build_json["number"]
    building = build_json["building"]
    in_progress = build_json["inProgress"]
    result = build_json["result"]
    timestamp = build_json["timestamp"]

    actions = build_json["actions"]
    causes = next((action["causes"] for action in actions if action.get("causes") is not None), None)
    user_id = next((cause["userId"] for cause in causes if cause.get("userId") is not None), None)

    print(number, building, in_progress, result, timestamp, user_id)
    print(get_build_params(build_json))


def get_last_build(job) -> int:
    return job["lastBuild"]["number"]


def to_yaml(job_name, params):
    return yaml.dump({"job": job_name, "params": params})
