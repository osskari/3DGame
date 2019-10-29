from GameObjects.GameCube import GameCube

class SandCube(GameCube):
    def __init__(self, position):
        # Placeholders, values, mega vera hardcoded því þau breytast aldrei, nema kannski texture skoða það
        super().__init__(position, [1, 2, 3], (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), 1)

    def hit(self):
        self.hp -= 30

    def get_texture(self):
        if self.hp > 70:
            return self.textures[0]
        elif self.hp > 40:
            return self.textures[1]
        else:
            return self.textures[2]
