"""
:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.start import Start
import logging.config

logging.config.fileConfig('data/conf/logging.conf')


def main():
    start = Start()


if __name__ == "__main__":
    main()
