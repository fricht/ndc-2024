import pyxel

pyxel.init(256, 256, 'lol')

pyxel.load('4.pyxres')

tilemap = pyxel.tilemaps[0]
images = pyxel.images[tilemap.imgsrc]

slime_coord = tilemap.pget(129, 127)
slime = images.pget(slime_coord[0], slime_coord[1])

pyxel.bltm(0, 0, tilemap, 0, 0, 256, 256)
pyxel.show()