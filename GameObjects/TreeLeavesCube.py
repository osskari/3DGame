from GameObjects.GameCube import GameCube

class TreeLeavesCube(GameCube):
    def __init__(self, position):
        super().__init__(position)
        # Öll hardcoded values eru placeholder
        self.texture = 1 #breyta tölum seinna sem matchar GL_TEXTURE id
        self.diffuse = (1.0, 1.0, 1.0)
        self.specular = (1.0, 1.0, 1.0)
        self.shininess = 4

    def hit(self):
        self.hp -= 60

    def get_texture(self):
        return self.texture