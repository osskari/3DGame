class GameCube: #placeholder name
    def __init__(self, position, textures, diffuse, specular, shininess):
        self.position = position
        self.hp = 100
        self.scale = (0.5, 0.5, 0.5) #Random tölur, breyta seinna
        self.textures = textures
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def isDestroyed(self):
        """
        Check if cube has been destroyed
        """
        return True if self.hp <= 0 else False

    # Default hit method, subclasses override for different behavior
    def hit(self):
        self.hp -= 20