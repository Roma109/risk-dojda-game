from game_objects import GameObject
from player import Human

# TODO: переписать спрайт груп для мира
class World:

    def __init__(self):
        self.game_objects = dict()
        self.humans = []

    def get_obj(self, pos):
        for obj in self.game_objects:
            if obj.is_inside(pos):
                return obj

    def add_object(self, obj: GameObject):
        self.game_objects[obj.id] = obj

    def remove_object(self, obj: GameObject):
        del self.game_objects[obj.id]

    def add_human(self, human: Human):
        self.humans.append(human)

    def remove_human(self, human: Human):
        self.humans.remove(human)
