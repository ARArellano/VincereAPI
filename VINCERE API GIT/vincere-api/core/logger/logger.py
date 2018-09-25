import logging
import os
from logging.handlers import RotatingFileHandler

LOGGER_NAME = "vincere.api"


def setup_logging(logger_name=LOGGER_NAME, logdir="logs", logfile="vicere_api.log",
                  scrnlog=False, txtlog=True, loglevel=logging.DEBUG):
    logdir = os.path.abspath(logdir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    log = logging.getLogger(logger_name)
    log.setLevel(loglevel)

    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s %(process)d %(filename)s:%(lineno)d  :: %(message)s")

    if txtlog:
        txt_handler = RotatingFileHandler(os.path.join(logdir, logfile), mode='a',
                                          maxBytes=1024 * 1024 * 3, backupCount=20)
        txt_handler.setFormatter(log_formatter)
        log.addHandler(txt_handler)
        log.info("Logger initialized.")

    if scrnlog:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        log.addHandler(console_handler)
