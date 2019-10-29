from GameObjects.GameCube import GameCube

class TreeCube(GameCube):
    def __init__(self, position):
        super().__init__(position, [1, 2, 3], (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), 1)

    def get_texture(self):
        if self.hp > 90:
            return self.textures[0]
        elif self.hp > 50:
            return self.textures[1]
        else:
            return self.textures[2]