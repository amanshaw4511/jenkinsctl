import json

from rich.console import Console
from datetime import datetime
from dateutil import tz


def get_console():
    return Console()


def format_timestamp(epoch_timestamp):
    # Convert epoch timestamp to a naive datetime object
    naive_dt = datetime.fromtimestamp(epoch_timestamp / 1000)

    # Get the local timezone
    local_tz = tz.tzlocal()

    # Convert naive datetime to local timezone
    local_dt = naive_dt.astimezone(local_tz)

    # Format the datetime object to a string
    return local_dt.strftime('%Y-%m-%d %H:%M')


def print_json(dict_obj):
    json_str = json.dumps(dict_obj)
    get_console().print_json(json_str)
