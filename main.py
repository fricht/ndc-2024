import pyxel
import random


SCREEN_SIZE = 128 * 2

TILE_SIZE = 8

TRANSPARENT = 5

COLLISIONNABLES = {
    # block
    (8, 216),
    (16, 216),
    (24, 216),
    (8, 224),
    (16, 224),
    (24, 224),
    (8, 232),
    (16, 232),
    (24, 232),
    # block fin vertical
    (0, 216),
    (0, 224),
    (0, 232),
    # poutre horizontale
    (24, 200),
    (32, 200),
    (40, 200)
}
COLLISIONNABLES = set(map(lambda x: (int(x[0]/TILE_SIZE), int(x[1] / TILE_SIZE)), COLLISIONNABLES))
CHARACTER = (0, int(104/TILE_SIZE))
PIECE = (int(32/TILE_SIZE), int(160/TILE_SIZE))

PIECE_SPRITE = (
    (32, 160),
    (40, 160),
    (48, 160),
    (56, 160),
)

JUMP = (32, 176)

ETOILE3 = (8, 192)
ETOILE5 = (16, 192)

SLIME_ANIM_LENGTH = 6
SLIME_ANIM = (
    104,
    112,
)



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

    def set_at(self, vec):
        self.x = vec.x
        self.y = vec.y
        return self

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
        return not (box.x >= self.x + self.width or box.x + box.width <= self.x or box.y >= self.y + self.height or box.y + box.height <= self.y)

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
        title = 'Slime Quest !'
        pyxel.text(SCREEN_SIZE / 2 - (int(len(title) * 2)), SCREEN_SIZE / 2, title, self.txt_col)
        play = 'Appuyez sur espace pour jouer...'
        pyxel.text(SCREEN_SIZE / 2 - (int(len(play) * 2)), SCREEN_SIZE / 2 + 10, play, self.txt_col)


class GameOver(Screen):
    def __init__(self, game, score, reason):
        self.game = game
        self.score = score
        self.cls_col = 5
        self.reason = reason
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.game.change_screen(MainMenu)

    def render(self):
        score = 'Score : %i' % self.score
        returnmenu = 'Appuyez sur espace pour recommencer'
        pyxel.text((SCREEN_SIZE / 2) - int(len(self.reason) * 2), (SCREEN_SIZE / 2) - 5, self.reason, 0)
        pyxel.text((SCREEN_SIZE / 2) - int(len(score) * 2), (SCREEN_SIZE / 2) + 5, score, 0)
        pyxel.text((SCREEN_SIZE / 2) - int(len(returnmenu) * 2), (SCREEN_SIZE / 2) + 15, returnmenu, 0)

class Character:
    SPEED = 3
    GRAVITY = 1
    JUMP_HEIGHT = -7
    COIL_JUMP_HEIGHT = -12

    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.hitbox = Box(x, y, TILE_SIZE, TILE_SIZE)
        self.velocity = Vector2(0, 0)
        self.can_jump = True
        self.score = 0
        self.anim_frame = 0
        self.anim_interval = 4

    def update(self, boxes, pieces, etoiles3, etoiles5, coils):
        self.velocity.x = int(pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT)) * self.SPEED
        self.velocity.y += self.GRAVITY
        if self.can_jump and (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_UP)):
            self.velocity.y = self.JUMP_HEIGHT
            self.can_jump = False
        self.pos.x += self.velocity.x
        for box in boxes:
            if box.is_box_colliding(self.hitbox.set_at(self.pos)):
                if self.velocity.x > 0:
                    self.pos.x = box.x - self.hitbox.width
                else:
                    self.pos.x = box.x + box.width
                self.velocity.x = 0
                self.can_jump = True
        self.pos.y += self.velocity.y
        for box in boxes:
            if box.is_box_colliding(self.hitbox.set_at(self.pos)):
                if self.velocity.y > 0:
                    self.pos.y = box.y - self.hitbox.height
                else:
                    self.pos.y = box.y + box.height
                self.velocity.y = 0
                self.can_jump = True
        collected = set()
        for coin in pieces:
            if coin.is_box_colliding(self.hitbox.set_at(self.pos)):
                self.score += 1
                collected.add(coin)
        for coin in collected:
            pieces.remove(coin)
        collected = set()
        for coin in etoiles3:
            if coin.is_box_colliding(self.hitbox.set_at(self.pos)):
                self.score += 3
                collected.add(coin)
        for coin in collected:
            etoiles3.remove(coin)
        collected = set()
        for coin in etoiles5:
            if coin.is_box_colliding(self.hitbox.set_at(self.pos)):
                self.score += 5
                collected.add(coin)
        for coin in collected:
            etoiles5.remove(coin)
        for coil in coils:
            if coil.is_box_colliding(self.hitbox.set_at(self.pos)):
                self.velocity.y = self.COIL_JUMP_HEIGHT
        ## ANIMATION
        self.anim_frame += 1
        if self.anim_frame > SLIME_ANIM_LENGTH * self.anim_interval:
            self.anim_frame = 0

    def draw(self, camera):
        camera.lerp_to(self.pos, 0.08)
        pyxel.blt(camera.transformX(self.pos.x), camera.transformY(self.pos.y), 0, int(self.anim_frame / self.anim_interval) * 8, SLIME_ANIM[int(self.velocity.x <= 0)], TILE_SIZE, TILE_SIZE, colkey=TRANSPARENT)
        pyxel.text(2, 2, "Score : %i" % self.score, 0)


class Game(Screen):
    def __init__(self, game):
        self.cls_col = TRANSPARENT + 1
        self.game = game
        pyxel.load("4.pyxres")
        self.tilemap = pyxel.tilemaps[0]
        ##
        init_pos = self.get_collisionnables()
        self.camera = Camera(init_pos.x, init_pos.y)
        ##
        self.player = Character(init_pos.x, init_pos.y)
        ## animation
        self.pframe = 0
        ## timer
        self.timer = 20 * 30

    def get_collisionnables(self):
        self.boxes = set()
        self.pieces = set()
        self.etoile3 = set()
        self.etoile5 = set()
        self.coils = set()
        spawn_point = Vector2(0, 0)
        for x in range(self.tilemap.width):
            for y in range(self.tilemap.height):
                if self.tilemap.pget(x, y) in COLLISIONNABLES:
                    self.boxes.add(Box(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
                elif self.tilemap.pget(x, y) == CHARACTER:
                    spawn_point = Vector2(TILE_SIZE * x, TILE_SIZE * y)
                    self.tilemap.pset(x, y, (0, 0))
                elif self.tilemap.pget(x, y) == PIECE:
                    self.pieces.add(Box(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
                    self.tilemap.pset(x, y, (0, 0))
                elif self.tilemap.pget(x, y) == tuple(map(lambda x: x / 8, ETOILE3)):
                    self.etoile3.add(Box(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
                    self.tilemap.pset(x, y, (0, 0))
                elif self.tilemap.pget(x, y) == tuple(map(lambda x: x / 8, ETOILE5)):
                    self.etoile5.add(Box(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
                    self.tilemap.pset(x, y, (0, 0))
                elif self.tilemap.pget(x, y) == tuple(map(lambda x: x / 8, JUMP)):
                    self.coils.add(Box(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
                    self.tilemap.pset(x, y, (int(JUMP[0] / 8) + 1, int(JUMP[1] / 8)))
        return spawn_point

    def render_coins(self):
        frame = PIECE_SPRITE[int(self.pframe / 4)]
        self.pframe += 1
        if self.pframe >= 4 * len(PIECE_SPRITE):
            self.pframe = 0
        for box in self.pieces:
            pyxel.blt(self.camera.transformX(box.x), self.camera.transformY(box.y), 0, frame[0], frame[1], TILE_SIZE, TILE_SIZE)
        for box in self.etoile3:
            pyxel.blt(self.camera.transformX(box.x), self.camera.transformY(box.y), 0, ETOILE3[0], ETOILE3[1], TILE_SIZE, TILE_SIZE)
        for box in self.etoile5:
            pyxel.blt(self.camera.transformX(box.x), self.camera.transformY(box.y), 0, ETOILE5[0], ETOILE5[1], TILE_SIZE, TILE_SIZE)

    def update(self):
        self.player.update(self.boxes, self.pieces, self.etoile3, self.etoile5, self.coils)
        self.timer -= 1
        if self.timer < 1:
            self.game.change_screen(GameOver, self.player.score, 'Time Out !')
        if self.player.pos.y > (256 * TILE_SIZE):
            self.game.change_screen(GameOver, self.player.score, 'Game Over !')

    def render(self):
        pyxel.bltm(self.camera.transformX(0), self.camera.transformY(0), self.tilemap, 0, 0, 256 * TILE_SIZE, 256 * TILE_SIZE)
        self.render_coins()
        self.player.draw(self.camera)
        pyxel.text(2, 9, 'Timer : %is' % (self.timer / 30), 0)




if __name__ == '__main__':
    game = MainGame()
    pyxel.init(SCREEN_SIZE, SCREEN_SIZE, 'Chicken Quest', fps=30)
    pyxel.run(game.update, game.render)
