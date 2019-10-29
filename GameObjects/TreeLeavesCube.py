from GameObjects.GameCube import GameCube

class TreeLeavesCube(GameCube):
    def __init__(self, position):
        super().__init__(position, 1, (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), 1)

    def hit(self):
        self.hp -= 60

    # Tree leaves only have one texture
    def get_texture(self):
        return self.texture