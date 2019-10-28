class CircularObject:
    def __init__(self, textureId, position):
        self.diffuse = (1.0, 1.0, 1.0)
        self.specular = (1.0, 1.0, 1.0)
        self.shininess = 1
        self.texture = textureId
        self.position = position


    