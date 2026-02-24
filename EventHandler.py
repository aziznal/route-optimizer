from typing import List, Tuple
import pygame

from PygameSettings import MouseInputType

from City import City


# REFACTOR: there's gotta be a better way than global vars.
# saving state of mouse rightclick
mouse_already_right_clicked: bool = False
prev_mouse_pos: Tuple[int, int] = None


def _handle_mouse_events(events: List[pygame.event.Event], city: City) -> None:
    """
    events: List of events at current timepoint

    city: City class which can create/remove/connect buildings

    This method handles mouse events such as left click or right click
    """

    global mouse_already_right_clicked
    global prev_mouse_pos

    current_mouse_pos = pygame.mouse.get_pos()

    # Pass mousepos to highlight hovered building
    city.set_highlighted_building(current_mouse_pos)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MouseInputType.LEFT_CLICK:
                city.create_building(current_mouse_pos)

            elif event.button == MouseInputType.RIGHT_CLICK:
                if mouse_already_right_clicked:
                    city.connect_buildings(
                        prev_mouse_pos,
                        current_mouse_pos,
                        bidirectional=False,
                        verbose=False,
                    )

                    mouse_already_right_clicked = False

                else:
                    mouse_already_right_clicked = True
                    prev_mouse_pos = current_mouse_pos

            elif event.button == MouseInputType.MIDDLE_CLICK:
                city.remove_building(current_mouse_pos)

            elif event.button == MouseInputType.SCROLL_UP:
                print(f"scroll up")

            elif event.button == MouseInputType.SCROLL_DOWN:
                print(f"scroll down")


def _handle_quit_events(events: List[pygame.event.Event]) -> None:
    """
    events: List of events at current timepoint
    """

    for event in events:
        if event.type == pygame.QUIT:
            exit()

        if pygame.key.get_pressed()[pygame.K_q]:
            exit()


def handle_events(city: City) -> None:
    """
    city: City class which can create/remove/connect buildings

    This function calls all other event handler functions in EventHandler and
    passes an events (pygame.event.Event) object to them

    """

    events = pygame.event.get()

    _handle_quit_events(events)

    _handle_mouse_events(events, city)
