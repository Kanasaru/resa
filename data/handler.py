import pygame
import xml.etree.ElementTree as ET


class GameDataHandler(object):
    def __init__(self):
        self._resources = {
            "Wood": 0,
            "Stone": 0,
            "Marble": 0,
            "Tools": 0,
            "Gold": 0,
        }
        self._world_data = None
        self._game_time = 0
        self._game_timer = None
        self._play_time = 0
        self._play_timer = None

    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, res: dict):
        for key, value in res.items():
            if key in self._resources:
                self._resources[key] = int(value)
            else:
                raise KeyError(f"'{key}' with '{value}' not in resources")

    @property
    def game_time(self):
        return self._game_time

    @game_time.setter
    def game_time(self, time):
        self._game_time = time

    @property
    def play_time(self):
        return self._play_time

    @play_time.setter
    def play_time(self, time):
        self._play_time = time

    @property
    def world_data(self):
        return self._world_data

    @world_data.setter
    def world_data(self, data: tuple[pygame.Rect, dict]):
        self._world_data = data

    def start_play_time(self):
        self._play_timer = pygame.time.Clock()
        self._play_timer.tick()

    def start_game_time(self):
        self._game_timer = pygame.time.Clock()
        self._game_timer.tick()

    def update(self):
        if self._play_timer is not None:
            self._play_timer.tick()
            self.play_time += self._play_timer.get_time() / 1000

        if self._game_timer is not None:
            self._game_timer.tick()
            self.game_time += self._game_timer.get_time() / 1000

    def read_from_file(self, filepath: str):
        tree = ET.parse(filepath)
        root = tree.getroot()
        # read world info
        rect = None
        fields = []
        for rect_data in root.findall('rect'):
            x = int(rect_data.find('x').text)
            y = int(rect_data.find('y').text)
            width = int(rect_data.find('width').text)
            height = int(rect_data.find('height').text)
            rect = pygame.Rect(x, y, width, height)
        # read fields
        for field in root.findall('field'):
            pos = tuple(field.find('pos').text)
            sprite_data = tuple(field.find('sprite_data').text)
            solid = bool(field.find('solid').text)
            fields.append([pos, sprite_data, solid])

        self.world_data = (rect, fields)

    def save_to_file(self, filepath: str):
        root = ET.Element("data")
        # save resources
        resources = ET.SubElement(root, "resources")
        for key, value in self.resources.items():
            ET.SubElement(resources, "res", name=key).text = str(value)

        # save world
        world = ET.SubElement(root, "world")
        ET.SubElement(world, "rect", name="x").text = str(self.world_data[0].x)
        ET.SubElement(world, "rect", name="y").text = str(self.world_data[0].y)
        ET.SubElement(world, "rect", name="width").text = str(self.world_data[0].width)
        ET.SubElement(world, "rect", name="height").text = str(self.world_data[0].height)
        fields = ET.SubElement(world, "fields")
        for raw_field in self.world_data[1]:
            field = ET.SubElement(fields, "field")
            ET.SubElement(field, "data", name="pos").text = str(raw_field[0])
            ET.SubElement(field, "data", name="sprite_data").text = str(raw_field[1])
            ET.SubElement(field, "data", name="solid").text = str(raw_field[2])

        # write file
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
