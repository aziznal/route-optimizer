import pygame

from PygameSettings import MouseInputType


# REFACTOR: there's gotta be a better way than global vars.
# saving state of mouse rightclick
mouse_already_right_clicked = False
prev_mouse_pos = None


def _handle_mouse_events(events, on_mouse_left_click, on_mouse_right_click, on_mouse_middle_click, on_mouse_scroll):

    global mouse_already_right_clicked
    global prev_mouse_pos

    mouse_event = pygame.mouse.get_pressed(num_buttons=3)
    mouse_pos = pygame.mouse.get_pos()

    for event in events:

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == MouseInputType.LEFT_CLICK:
                on_mouse_left_click(mouse_pos)

            elif event.button == MouseInputType.RIGHT_CLICK:

                if mouse_already_right_clicked:
                    on_mouse_right_click(prev_mouse_pos, mouse_pos, bidirectional=False, verbose=False)
                    mouse_already_right_clicked = False

                else:
                    mouse_already_right_clicked = True
                    prev_mouse_pos = mouse_pos
                

            elif event.button == MouseInputType.MIDDLE_CLICK:
                on_mouse_middle_click(mouse_pos)

            elif event.button == MouseInputType.SCROLL_UP:
                on_mouse_scroll("up", mouse_pos)

            elif event.button == MouseInputType.SCROLL_DOWN:
                on_mouse_scroll("down", mouse_pos)


def _handle_quit_events(events):

    for event in events:

        if event.type == pygame.QUIT:
            exit()

        if pygame.key.get_pressed()[pygame.K_q]:
            exit()


def handle_events(on_mouse_left_click, on_mouse_right_click, on_mouse_middle_click, on_mouse_scroll):

    events = pygame.event.get()

    _handle_quit_events(events)

    _handle_mouse_events(events, on_mouse_left_click,
                         on_mouse_right_click, on_mouse_middle_click, on_mouse_scroll)
