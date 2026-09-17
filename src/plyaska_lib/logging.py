import logging
import os
from datetime import date

from src.plyaska_lib.config import settings


def logging_setup():
    env = settings

    log_dir = env.logging_dir_path
    if len(log_dir) > 0 and log_dir[-1] == "/":
        log_dir = log_dir[:-1]
    log_dir = f"{log_dir}/{date.today()}"
    # Create a 'logs' directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(log_dir, "internal.log"),
        level=logging.DEBUG,
        format="%(name)s %(asctime)s %(levelname)s %(message)s",
    )
