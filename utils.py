from typing import List, Any, Dict
import traceback
import json

import pygame

pygame.init()
pygame.font.init()



def create_text(text, font_size, color, bold=False) -> pygame.Surface:
    """
    Returns a pygame surface with the desired text in it
    """

    font_obj = pygame.font.SysFont("arial", font_size, bold=bold)

    return font_obj.render(text, True, color)



def confirm_hashes_are_unique(buildings: List) -> None:
    """
    Raises KeyError if any two objects in given list have identical hashes
    """

    hashes = [ hash(building) for building in buildings ]

    if len(set(hashes)) != len(hashes):
        raise KeyError("Found two matching hashes!")



def load_map(to_filename="default-map-buildings.json") -> Dict:
    """
    to_filename (string): name of file to load

    Loads and returns map with given filename as a dict. Returns empty dict if any exception occurs
    """

    try:
        with open(to_filename, 'r') as map_file:
            return json.load(map_file)


    except Exception as e:
        print(f"\nWARNING! Couldn't find file ({to_filename}).")
        traceback.print_exc()
        return { "data": [] }


def save_changes(data: List, map_name:str="default-map-buildings.json") -> None:
    """
    data: Data to save

    map_name: name of file where data will be saved

    Saves provided data into given filename
    """

    data_as_dict: Dict[str, List] = {
        "data": [
            {"x": building.x, "y": building.y, "connections": [[conn.x, conn.y] for conn in building.connections]} for building in data
        ]
    }

    with open(map_name, "w") as save_file:
        json.dump(data_as_dict, save_file, indent=4)
