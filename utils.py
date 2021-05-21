from typing import List, Any
import traceback
import pickle

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



def load_map(to_filename="default-map-buildings.p") -> List:
    """
    to_filename (string): name of file to load

    Loads and returns map with given filename. Returns empty list if any exception occurs
    """

    try:

        with open(to_filename, 'rb') as map_file:
            return pickle.load(map_file)

    except Exception as e:
        print(f"WARNING! Couldn't find file ({to_filename}).")
        traceback.print_exc()
        return []


def save_changes(data: Any, map_name:str="default-map-buildings.p") -> None:
    """
    data: Data to save

    map_name: name of file where data will be saved

    Saves provided data into given filename
    """

    with open(map_name, "wb") as save_file:
        pickle.dump(data, save_file)
