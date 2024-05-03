import pyxel
import random


SCREEN_SIZE = 128 * 2

TILE_SIZE = 8

TRANSPARENT = 5

COLLISIONNABLES = {
    (0,),
    (0,),
}



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

    def set_to(self, point):
        self.x = point.x
        self.y = point.y
        return self

    def lerp_to(self, point, a):
        self.x += a * (point.x - self.x)
        self.y += a * (point.y - self.y)
        return self



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
            self.game.change_screen(Game)
        self.t += 1
        if self.t > 30:
            self.t = 0
            self.gen_cols()

    def render(self):
        pyxel.rect(10, 10, 15, 15, self.txt_col)
        pyxel.text(SCREEN_SIZE / 2, SCREEN_SIZE / 2, 'Chicken Quest !', self.txt_col)
        pyxel.text(0, SCREEN_SIZE / 2 + 10, 'Press SPACE to play...', self.txt_col)


class Character:
    SPEED = 2
    GRAVITY = 1

    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.hitbox = Box(x, y, TILE_SIZE, TILE_SIZE)
        self.velocity = Vector2(0, 0)

    def update(self):
        self.velocity.x = int(pyxel.btn(pyxel.KEY_DOWN) - pyxel.btn(pyxel.KEY_UP)) * self.SPEED
        self.pos.x += self.velocity.x

    def draw(self, camera):
        camera.lerp_to(self.pos, 0.08)
        pyxel.blt(camera.transformX(self.pos.x), camera.transformY(self.pos.y), 0, 0, 104, TILE_SIZE, TILE_SIZE, colkey=TRANSPARENT)


class Game(Screen):
    def __init__(self, game):
        self.cls_col = TRANSPARENT + 1
        self.game = game
        pyxel.load("4.pyxres")
        self.tilemap = pyxel.tilemaps[0]
        ##
        init_pos_x, init_pos_y = 10, 50
        self.camera = Camera(init_pos_x, init_pos_y)
        ##
        self.get_collisionnables()
        ##
        self.player = Character(init_pos_x, init_pos_y)

    def get_collisionnables(self):
        self.boxes = set()
        for x in range(self.tilemap.width):
            for y in range(self.tilemap.height):
                if self.tilemap.pget(x, y) in COLLISIONNABLES:
                    self.boxes.add(Box(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE))

    def update(self):
        self.player.update()

    def render(self):
        pyxel.bltm(self.camera.transformX(0), self.camera.transformY(0), self.tilemap, 0, 0, 256, 256)
        self.player.draw(self.camera)




if __name__ == '__main__':
    game = MainGame()
    pyxel.init(SCREEN_SIZE, SCREEN_SIZE, 'Chicken Quest')
    pyxel.run(game.update, game.render)
