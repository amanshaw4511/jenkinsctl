import logging
from contextlib import contextmanager

from jenkinsctl.configs.config import settings
from jenkinsctl.configs.session import Session

log = logging.getLogger(__name__)

@contextmanager
def error_handler_and_session():
    server_url: str = settings.server_url
    username: str = settings.username
    api_key: str = settings.api_key

    session = None
    try:
        session = Session(server_url)
        session.auth = (username, api_key)
        yield session
    except Exception as e:
        log.debug(f"An error occurred", exc_info=e )
        print(f"An error occurred, run same command with --verbose flag to print error details")
    finally:
        if session:
            session.close()