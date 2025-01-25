"""
Setting up a standard logger with colored text.

## Usage examples

```python
## without log file
logger = hsg.init_logger("harrix-pyssg")
logger.debug("This is a debug-level message")
logger.info("This is an info-level message")
logger.warning("This is a warning-level message")
logger.error("This is an error-level message")
logger.critical("This is a critical-level message")

## with log file
logger = hsg.init_logger("harrix-pyssg", True)
logger.debug("This is a debug-level message")
logger.info("This is an info-level message")
logger.warning("This is a warning-level message")
logger.error("This is an error-level message")
logger.critical("This is a critical-level message")
```

Inside the library `harrix-pyssg`:

```python
# without log file
logger = init_logger("harrix-pyssg")
logger.debug("This is a debug-level message")
logger.info("This is an info-level message")
logger.warning("This is a warning-level message")
logger.error("This is an error-level message")
logger.critical("This is a critical-level message")

# with log file
logger = init_logger("harrix-pyssg", True)
logger.debug("This is a debug-level message")
logger.info("This is an info-level message")
logger.warning("This is a warning-level message")
logger.error("This is an error-level message")
logger.critical("This is a critical-level message")
```
"""
import datetime
import logging


def init_logger(name, is_file_handler=False):
    class CustomFormatter(logging.Formatter):
        normal = "\x1b[0m"
        green = "\x1b[32m"
        blue = "\x1b[34m"
        red = "\x1b[31m"
        red_background = "\x1b[41m"
        reset = "\x1b[0m"

        def __init__(self, fmt):
            super().__init__()
            self.fmt = fmt
            self.FORMATS = {
                logging.DEBUG: self.normal + self.fmt + self.reset,
                logging.INFO: self.green + self.fmt + self.reset,
                logging.WARNING: self.blue + self.fmt + self.reset,
                logging.ERROR: self.red + self.fmt + self.reset,
                logging.CRITICAL: self.red_background + self.fmt + self.reset,
            }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(logging.DEBUG)

    fmt_stdout_handler = "%(levelname)-8s | %(message)s (%(filename)s:%(lineno)d)"
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter(fmt_stdout_handler))
    custom_logger.addHandler(stdout_handler)

    if is_file_handler:
        fmt_file_handler = (
            "%(asctime)s | %(levelname)-8s | %(message)s (%(filename)s:%(lineno)d)"
        )
        today = datetime.date.today()
        file_handler = logging.FileHandler(
            "{}_{}.log".format(name, today.strftime("%Y_%m_%d"))
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(fmt_file_handler))
        custom_logger.addHandler(file_handler)

    return custom_logger


logger = init_logger("harrix-pyssg")
