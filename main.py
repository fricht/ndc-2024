import pyxel



class MainGame:
    def __init__(self):
        self.screen = MainMenu()

    def update(self):
        self.screen.update()

    def render(self):
        pyxel.cls(self.screen.cls_col)
        self.screen.render()

    def change_screen(self, new_screen, *args, **kwargs):
        self.screen = new_screen(self, *args, **kwargs)



class Screen: # abstract class
    cls_col = 1
    def __init__(self, game):
        self.game = game
    def update(self):
        pass
    def render(self):
        pass


class MainMenu(Screen):
    def __init__(self):
        self.bg_col = 1
        self

    def update(self):
        pass

    def render(self):
        pyxel.rect(10, 10, 15, 15, 1)




if __name__ == '__main__':
    game = MainGame()
    pyxel.init(128, 128, 'Window Name')
    pyxel.run(game.update, game.render)
