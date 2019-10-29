class GameCube: #placeholder name
    def __init__(self, position):
        self.position = position
        self.hp = 100
        self.scale = (0.5, 0.5, 0.5) #Random tölur, breyta seinna

    def isDestroyed(self):
        """
        Check if cube has been destroyed
        """
        return True if self.hp <= 0 else False

    def hit(self):
        self.hp -= 20