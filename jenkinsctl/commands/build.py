from io import TextIOWrapper

from jenkinsctl.configs.session import Session
from jenkinsctl.jenkins.job import build_job
from typing import List
import yaml
import sys


def get_config_from_yaml(file):
    config_data = None
    try:
        with open(file.name, "r") as config_file:
            config_data = yaml.safe_load(config_file)  # Use safe_load for YAML
    except FileNotFoundError:
        print(f"Error: Configuration file '{file}' not found.")
        sys.exit()
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in '{file}': {e}")
        sys.exit()

    return config_data


def get_conf(file, params):
    config = get_config_from_yaml(file)
    override_params(params, config)
    return config


def override_params(params, file_config):
    for param in params:
        name, value = param.split('=')
        file_config['params'][name] = value


def build_handler(session: Session, file: TextIOWrapper, params: List[str]):
    conf = get_conf(file, params)
    print(conf)
    build_job(session, conf["job"], conf["params"])
