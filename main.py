"""
:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import logging.config
from data.start import Start


def main():
    logging.config.fileConfig('data/conf/logging.conf')
    start = Start()


if __name__ == "__main__":
    main()
