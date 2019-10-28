class SandCube(GameCube):
    def __init__(self, position):
        super().__init__(position)
        # Öll hardcoded values eru placeholder
        self.textures = [1, 2, 3] #breyta tölum seinna sem matchar GL_TEXTURE id
        self.diffuse = (1.0, 1.0, 1.0)
        self.specular = (1.0, 1.0, 1.0)

    def hit(self):
        self.hp -= 40