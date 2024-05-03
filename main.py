import pyxel



class MainGame:
    def __init__(self):
        self.screen = MainMenu()

    def update(self):
        self.screen.update()

    def render(self):
        pyxel.cls(0)
        self.screen.render()



class Screen: # abstract class
    def update(self):
        pass
    def render(self):
        pass


class MainMenu(Screen):
    def render(self):
        pyxel.rect(10, 10, 15, 15, 1)




if __name__ == '__main__':
    game = MainGame()
    pyxel.init(128, 128, 'Window Name')
    pyxel.run(game.update, game.render)
