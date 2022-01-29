"""
:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import logging.config
import src.game


if __name__ == "__main__":
    logging.config.fileConfig('data/conf/logging.conf')
    game = src.game.Game()
    game.run()
