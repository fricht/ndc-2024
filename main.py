import pyxel
import random


SCREEN_SIZE = 128 * 2



class MainGame:
    def __init__(self):
        self.screen = MainMenu(self)

    def update(self):
        self.screen.update()

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



class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def transformX(self, point):
        return point - self.x + SCREEN_SIZE / 2

    def transformY(self, point):
        return point - self.y + SCREEN_SIZE / 2

    def transform(self, point):
        return Vector2(self.transformX(point.x), self.transformX(point.y))



class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def copy(self):
        return Vector2(self.x, self.y)

    def get_length(self):
        return pyxel.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        d = self.get_length()
        self.x /= d
        self.y /= d
        return self


class Box:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # center
    @property
    def center(self):
        return Vector2(self.x + self.width / 2, self.y + self.height / 2)
    @center.setter
    def center(self, value):
        self.x = value.x - self.width / 2
        self.y = value.y - self.height / 2

    def is_point_inside(self, point):
        return (point.x > self.x and point.x < self.x + self.width and point.y > self.y and point.y < self.y + self.height)

    def is_box_colliding(self, box):
        return not (box.x > self.x + self.width or box.x + box.width < self.x or box.y > self.y + self.height or box.y + box.height < self.y)

    def render(self, color, camera):
        if camera == None:
            pyxel.rect(self.x, self.y, self.width, self.height, color)
        else :
            pyxel.rect(camera.transformX(self.x), camera.transformY(self.y), self.width, self.height, color)



class MainMenu(Screen):
    def __init__(self, game):
        self.game = game
        self.gen_cols()
        self.t = 0

    def gen_cols(self):
        self.cls_col = random.choice(range(16))
        other_cols = list(range(16))
        other_cols.remove(self.cls_col)
        self.txt_col = random.choice(other_cols)

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.game.change_screen(MainMenu)
        self.t += 1
        if self.t > 60:
            self.t = 0
            self.gen_cols()

    def render(self):
        pyxel.rect(10, 10, 15, 15, self.txt_col)
        pyxel.text(SCREEN_SIZE / 2, SCREEN_SIZE / 2, 'Chicken Quest !', self.txt_col)
        pyxel.text(0, SCREEN_SIZE / 2 + 10, 'Press SPACE to play...', self.txt_col)




if __name__ == '__main__':
    game = MainGame()
    pyxel.init(SCREEN_SIZE, SCREEN_SIZE, 'Chicken Quest')
    pyxel.run(game.update, game.render)
