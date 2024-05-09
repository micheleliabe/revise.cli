import logging
from rich.logging import RichHandler

FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(
    filename="revise.log",
    encoding="utf-8",
    level="DEBUG",
    format=FORMAT,
    datefmt="[%Y-%m-%d %H:%M:%S]",
    # handlers=[RichHandler(show_path=False, show_time=True,
    #                       omit_repeated_times=False)]
)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

log = logging.getLogger("revise")


def disable_logging():
    log.disabled = True


def enable_logging():
    log.disabled = False
