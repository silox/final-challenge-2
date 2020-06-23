BACKGROUND = 'resources/gfx/backgrounds/bg-level0.png'
MUSIC = 'resources/sfx/themes/intro-music.mp3'


def bsod_button_click(app):
    app.current_level.get_object('bsod_background').enable()
    app.current_level.get_object('bsod_button').disable()
    app.change_music('resources/sfx/themes/bsod.mp3')


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
    }
}
