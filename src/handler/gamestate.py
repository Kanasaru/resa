import pygame


class GameStateHandler(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.exit_resa = False
        self.current_menu = None
        self.game_running = False
        self.pause_game = False
        # building menu
        self.cursor_over_icons = False
        self.build_menu_open = False
        self.build_menu = -1
        # building mode
        self.place = False
        self.place_on = None
        self.building = False
        self.building_size = (3, 3)
        # mountains
        self.mountain_spawn_attempts = {
            'North_West': 0,
            'North': 0,
            'North_East': 0,
            'Center_West': 0,
            'Center': 0,
            'Center_East': 0,
            'South_West': 0,
            'South': 0,
            'South_East': 0,
        }

    def reset_mountain_spawn_attempts(self):
        self.mountain_spawn_attempts = {
            'North_West': 0,
            'North': 0,
            'North_East': 0,
            'Center_West': 0,
            'Center': 0,
            'Center_East': 0,
            'South_West': 0,
            'South': 0,
            'South_East': 0,
        }
