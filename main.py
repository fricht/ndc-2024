import pyxel
import math



SCREEN_SIZE = 128



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
        return math.sqrt(self.x ** 2 + self.y ** 2)

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
    def __init__(self):
        self.bg_col = 1
        self.fg_col = 2
        self.cls_col = 6
        self.is_hovered = False

    def update(self):
        pass

    def render(self):
        pyxel.rect(10, 10, 15, 15, self.bg_col)




if __name__ == '__main__':
    game = MainGame()
    pyxel.init(128, 128, 'Window Name')
    pyxel.run(game.update, game.render)
