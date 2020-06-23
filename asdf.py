import sys
import pygame as pg


BACKGROUND = pg.Color("darkslategray")
SCREEN_SIZE = (500, 500)
FPS = 60


class App(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.text = self.make_text()

    def update(self):
        pass

    def make_text(self):
        text = FONT.render("Hello.", True, (0,0,0), pg.Color("white"))
        text.set_colorkey(pg.Color("white"))
        text.set_alpha(200)
        text_rect = text.get_rect(center=self.screen_rect.center)
        return text, text_rect

    def render(self):
        first_half = self.screen_rect.copy()
        first_half.w = self.screen_rect.centerx
        second_half = first_half.copy()
        second_half.x = self.screen_rect.centerx
        self.screen.fill(pg.Color("red"), first_half)
        self.screen.fill(pg.Color("green"), second_half)
        self.screen.blit(*self.text)
        pg.display.update()

    def event_loop(self):
        for event in pg.event.get():
           if event.type == pg.QUIT:
               self.done = True

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(FPS)


def main():
    global FONT
    pg.init()
    FONT = pg.font.Font(None, 120)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
