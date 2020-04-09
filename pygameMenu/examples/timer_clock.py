# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - TIMER CLOCK
Example file, timer clock with in-menu options.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

# Import libraries
import sys

sys.path.insert(0, '../../')

import datetime
import os
import pygame
from random import randrange

import pygameMenu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),
         'Author: @{0}'.format(pygameMenu.__author__),
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
FPS = 60
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
W_SIZE = 800  # Width of window size

surface = None
timer = None


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def mainmenu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    global surface
    surface.fill((40, 0, 40))


def reset_timer():
    """
    Reset timer.
    """
    global timer
    timer[0] = 0


class TestCallClassMethod(object):
    """
    Class call method.
    """

    @staticmethod
    def update_game_settings():
        """
        Class method.
        """
        print('Update game with new settings')


def change_color_bg(value, c=None, **kwargs):
    """
    Change background color.

    :param value: Selected option (data, index)
    :type value: tuple
    :param c: Color tuple
    :type c: tuple
    """
    color, _ = value
    if c == (-1, -1, -1):  # If random color
        c = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    if kwargs['write_on_console']:
        print('New background color: {0} ({1},{2},{3})'.format(color, *c))
    COLOR_BACKGROUND[0] = c[0]
    COLOR_BACKGROUND[1] = c[1]
    COLOR_BACKGROUND[2] = c[2]


def main(test=False):
    """
    Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Write help message on console
    for m in HELP:
        print(m)

    # Create window
    global surface
    surface = pygame.display.set_mode((W_SIZE, H_SIZE))
    pygame.display.set_caption('Example - Timer Clock')

    # Main timer and game clock
    clock = pygame.time.Clock()
    global timer
    timer = [0.0]
    dt = 1.0 / FPS
    timer_font = pygameMenu.font.get_font(pygameMenu.font.FONT_NEVIS, 100)

    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------

    # Timer
    timer_menu = pygameMenu.Menu(surface,
                                 dopause=False,
                                 font=pygameMenu.font.FONT_NEVIS,
                                 menu_alpha=85,
                                 menu_background_color=(0, 0, 0),  # Background color
                                 menu_height=H_SIZE * 0.65,
                                 menu_width=600,
                                 onclose=pygameMenu.events.RESET,  # If this menu closes (ESC) back to main
                                 selection_highlight_border_width=4,
                                 title='Timer Menu',
                                 title_background_color=(0, 0, 0),
                                 title_offset_y=5,  # Adds 5px to title vertical position
                                 widget_shadow=True,
                                 )

    # Add widgets
    timer_menu.add_button('Reset timer', reset_timer)

    # Adds a selector (element that can handle functions)
    timer_menu.add_selector(title='Change bgcolor',
                            values=[('Random', (-1, -1, -1)),  # Values of selector, call to change_color_bg
                                    ('Default', (128, 0, 128)),
                                    ('Black', (0, 0, 0)),
                                    ('Blue', COLOR_BLUE)],
                            default=1,  # Optional parameter that sets default item of selector
                            onchange=change_color_bg,  # Action when changing element with left/right
                            onreturn=change_color_bg,  # Action when pressing return on an element
                            # Optional parameters to change_color_bg function
                            write_on_console=True,
                            )
    timer_menu.add_button('Update game object', TestCallClassMethod().update_game_settings)
    timer_menu.add_button('Return to Menu', pygameMenu.events.BACK)
    timer_menu.add_button('Close Menu', pygameMenu.events.CLOSE)
    timer_menu.center_vertically()

    # Help menu
    help_menu = pygameMenu.TextMenu(surface,
                                    dopause=False,
                                    font=pygameMenu.font.FONT_FRANCHISE,
                                    menu_background_color=(30, 50, 107),  # Background color
                                    menu_height=600,  # Fullscreen
                                    menu_width=800,
                                    onclose=pygameMenu.events.DISABLE_CLOSE,  # Pressing ESC button does nothing
                                    text_align=pygameMenu.locals.ALIGN_CENTER,
                                    text_fontsize=35,
                                    title='Help',
                                    title_background_color=(120, 45, 30),
                                    title_font_size=60,
                                    widget_font_size=45,
                                    widget_offset_y=0.3,  # Percentage of height
                                    widget_shadow=True,
                                    widget_shadow_position=pygameMenu.locals.POSITION_SOUTHEAST,
                                    )
    help_menu.add_button('Return to Menu', pygameMenu.events.BACK)
    for m in HELP:
        help_menu.add_line(m)

    # About menu
    about_menu = pygameMenu.TextMenu(surface,
                                     dopause=False,
                                     draw_text_region_x=5,  # 5% margin
                                     font=pygameMenu.font.FONT_NEVIS,
                                     menu_height=400,
                                     menu_width=600,
                                     mouse_visible=False,
                                     onclose=pygameMenu.events.DISABLE_CLOSE,  # Disable menu close (ESC button)
                                     text_fontsize=20,
                                     title='About',
                                     title_background_color=COLOR_BLUE,
                                     title_font=pygameMenu.font.FONT_8BIT,
                                     title_font_size=30,
                                     widget_offset_y=0.3,  # Percentage of height
                                     widget_shadow=True,
                                     )
    about_menu.add_button('Return to Menu', pygameMenu.events.BACK)
    for m in ABOUT:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)

    # Main menu, pauses execution of the application
    main_menu = pygameMenu.Menu(surface,
                                bgfun=mainmenu_background,
                                enabled=False,
                                font=pygameMenu.font.FONT_NEVIS,
                                fps=FPS,
                                menu_alpha=90,
                                menu_height=400,
                                menu_width=600,
                                onclose=pygameMenu.events.CLOSE,
                                title='Main Menu',
                                title_background_color=(170, 65, 50),
                                title_offset_y=5,
                                )

    main_menu.add_button(timer_menu.get_title(), timer_menu)  # Add timer submenu
    main_menu.add_button(help_menu.get_title(), help_menu)  # Add help submenu
    main_menu.add_button(about_menu.get_title(), about_menu)  # Add about submenu
    main_menu.add_button('Exit', pygameMenu.events.EXIT)  # Add exit function
    main_menu.center_vertically()

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick clock
        clock.tick(FPS)
        timer[0] += dt

        # Paint background
        surface.fill(COLOR_BACKGROUND)

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.enable()

        # Draw timer
        time_string = str(datetime.timedelta(seconds=int(timer[0])))
        time_blit = timer_font.render(time_string, 1, COLOR_WHITE)
        time_blit_size = time_blit.get_size()
        surface.blit(time_blit, (int(W_SIZE / 2 - time_blit_size[0] / 2), int(H_SIZE / 2 - time_blit_size[1] / 2)))

        # Execute main from principal menu if is enabled
        main_menu.mainloop(events, disable_loop=test)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
