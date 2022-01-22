class GameStateHandler(object):
    def __init__(self):
        self.start_game = False
        self.load_game = False
        self.leave_game = False
        self.options = False
        self.start_editor = False
        self.leave_game = False
        self.exit_game = False
        self.map_load = False
        self.pause_game = False
        self.building = False
        self.building_size = (3, 3)
        self.place = False
        self.place_on = None
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
