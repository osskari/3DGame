from GameObjects.GameCube import GameCube

class TreeCube(GameCube):
    def __init__(self, position):
        super().__init__(position)
        # Öll hardcoded values eru placeholder
        self.textures = [1, 2, 3] #breyta tölum seinna sem matchar GL_TEXTURE id
        self.diffuse = (1.0, 1.0, 1.0)
        self.specular = (1.0, 1.0, 1.0)
        self.shininess = 4

    def get_texture(self):
        if self.hp > 90:
            return self.textures[0]
        elif self.hp > 50:
            return self.textures[1]
        else:
            return self.textures[2]