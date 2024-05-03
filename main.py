import pyxel

class Game:
    def __init__(self, width, height, title):
        pyxel.init(width, height, title=title)
        self.x = 0
        pyxel.run(self.update, self.render)
    
    def update(self):
        self.x = (self.x + 1) % pyxel.width
    
    def render(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)

Game(128, 128, 'lol ca marche')