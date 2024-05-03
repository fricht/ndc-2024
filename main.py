import pyxel

class Game:
    def __init__(self, width, height, title):
        pyxel.init(width, height, title=title)
        self.x = 0
        pyxel.run(self.update, self.render)
    
    def update(self):
        self.x = (self.x + 1) % pyxel.width
    
    def render(self):
        pyxel.cls(self.screen.cls_col)
        self.screen.render()

    def change_screen(self, new_screen, *args, **kwargs):
        self.screen = new_screen(self, *args, **kwargs)



class Screen: # abstract class
    cls_col = 0
    def __init__(self, game):
        self.game = game
    def update(self):
        pass
    def render(self):
        pass


class MainMenu(Screen):
    def __init__(self):
        self.bg_col = 1
        self.fg_col = 2
        self.cls_col = 6

    def update(self):
        pass

    def render(self):
        pyxel.rect(10, 10, 15, 15, self.bg_col)

Game(128, 128, 'lol ca marche')