## baseConfig setup

# import logging

# # Set up the logging configuration
# logging.basicConfig(
#     filename='etc/log/debug.log',
#     #encoding="utf-8",        # I'm getting a warning message? LSP problem? Think you need python 3.9;
#     filemode="a",            # a is default
#     level=logging.DEBUG,
#     format="{levelname} : {message} | {module}:{lineno} | {asctime}",
#     style="{",
#     datefmt="%Y.%m.%d %H:%M:%S %p",
# )

# # init the logger variable
# logger = logging.getLogger(__name__)
# # In the router.py script, we import logger variable;

# # First logger print
# logger.info('======== logger started ========')

# # It seems that the variable 'logger' needs to be specifically imported to work;


##############################################3

## dictConfig setup

import logging
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {
        'format1': {
          "format": "{levelname} : {message} | {module}:{lineno} | {asctime}",
          "style": "{"
          # For this style, but denote the style;
        },
        'format2': {
          # 'format': '%(levelname)s : %(message)s | %(module)s:%(lineno)s | %(asctime)s',
          'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
          # "style": "%"
          # For this style, appears to be optional
        }
        # The options for style are "%", "$", or "{".

    },

    'handlers': {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "format1",
        },
        "console2": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "format1",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "etc/log/debug.log",
            "formatter": "format1",
        },
    },

    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "file"
        ]
    },

    "loggers": {
        "logger": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": False,
        },
        "logger2": {
            "level": "DEBUG",
            "handlers": ["console2"],
            "propagate": False,
        }

    },
})

root = logging.getLogger("root")
logger = logging.getLogger("extra")

logger.info('======== extra logger started ========')
root.info('======== root logger started ========')
