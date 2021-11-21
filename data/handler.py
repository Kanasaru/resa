import pygame
import xml.etree.ElementTree as ET


class GameDataHandler(object):
    def __init__(self):
        self.__resources = {
            "Wood": 0,
            "Stone": 0,
            "Marble": 0,
            "Tools": 0,
            "Gold": 0,
        }
        self.__world_data = None
        self.__game_time = 0
        self.__game_timer = None
        self.__play_time = 0
        self.__play_timer = None

    def update_resources(self, resources: dict):
        for key, value in resources.items():
            if key in self.__resources:
                self.__resources[key] = int(value)
            else:
                print(f"'{key}' with '{value}' not in resources")

    def set_game_time(self, time):
        self.__game_time = time

    def set_play_time(self, time):
        self.__play_time = time

    def set_world_data(self, data: tuple[pygame.Rect, dict]):
        self.__world_data = data

    def start_play_time(self):
        self.__play_timer = pygame.time.Clock()
        self.__play_timer.tick()

    def start_game_time(self):
        self.__game_timer = pygame.time.Clock()
        self.__game_timer.tick()

    def update(self):
        if self.__play_timer is not None:
            self.__play_timer.tick()
            self.__play_time += self.__play_timer.get_time() / 1000

        if self.__game_timer is not None:
            self.__game_timer.tick()
            self.__game_timer += self.__game_timer.get_time() / 1000

    def read_from_file(self, filepath: str):
        tree = ET.parse(filepath)
        root = tree.getroot()

    def save_to_file(self, filepath: str):
        root = ET.Element("data")
        # save resources
        resources = ET.SubElement(root, "resources")
        for key, value in self.__resources.items():
            ET.SubElement(resources, "res", name=key).text = str(value)

        # save world
        world = ET.SubElement(root, "world")
        ET.SubElement(world, "rect", name="x").text = str(self.__world_data[0].x)
        ET.SubElement(world, "rect", name="y").text = str(self.__world_data[0].y)
        ET.SubElement(world, "rect", name="width").text = str(self.__world_data[0].width)
        ET.SubElement(world, "rect", name="height").text = str(self.__world_data[0].height)
        fields = ET.SubElement(world, "fields")
        for field_obj in self.__world_data[1]:
            field = ET.SubElement(fields, "field")
            ET.SubElement(field, "data", name="pos").text = str(field_obj.position())
            ET.SubElement(field, "data", name="sprite_data").text = str((field_obj.sprite_sheet_id, field_obj.sprite_id))
            ET.SubElement(field, "data", name="solid").text = str(field_obj.solid)

        # write file
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
