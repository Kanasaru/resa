"""
:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import logging.config
import src
import src.start


def main():
    logging.config.fileConfig('data/conf/logging.conf')
    start = src.start.Start()


if __name__ == "__main__":
    main()
