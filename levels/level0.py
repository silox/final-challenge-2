# Welcome screen

def bsod_button_click(app):
    app.current_level.get_object('bsod_background').enable()
    app.current_level.get_object('bsod_button').disable()
    app.change_music('resources/sfx/themes/bsod.mp3')


def quit_click(app):
    app.quit = True


BACKGROUND = 'resources/gfx/backgrounds/bg-level0.png'
MUSIC = 'resources/sfx/themes/intro-music.mp3'

OBJECTS = {
    'bsod_button': {
        'type': 'button',
        'options': {
            'gui_options': (500, 630, 200, 70),
            'on_click': bsod_button_click,
            'content': {
                'type': 'text',
                'options': {
                    'text': 'Vstúpiť',
                    'font': 'Times New Roman',
                    'size': 30,
                }
            }
        }
    },

    'bsod_background': {
        'type': 'image',
        'options': {
            'gui_options': (0, 0),
            'image_path': 'resources/gfx/backgrounds/bsod.png',
            'visible': False,
        }
    },

    'result_screen_background': {
        'type': 'image',
        'options': {
            'gui_options': (0, 0),
            'image_path': 'resources/gfx/backgrounds/bg-results.png',
            'visible': False,
        }
    },

    'result_text': {
        'type': 'text',
        'options': {
            'gui_options': (640, 280),
            'text': 'Your journey is over, congratulations! Final score: $',
            'max_len': 40,
            'color': (255, 255, 255),
            'font': 'Helvetica',
            'size': 40,
        }
    },

    'quit_button': {
        'type': 'button',
        'options': {
            'gui_options': (500, 600, 200, 70),
            'on_click': quit_click,
            'content': {
                'type': 'text',
                'options': {
                    'text': 'Quit',
                    'font': 'Times New Roman',
                    'size': 30,
                }
            }
        }
    },

}
