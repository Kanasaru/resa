"""
:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
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
