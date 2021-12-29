"""
:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""

from data.handlers.locals import LocalsHandler
from data.start import Start
import logging.config


def main():
    logging.config.fileConfig('data/conf/logging.conf')
    LocalsHandler.init()
    start = Start()


if __name__ == "__main__":
    main()
