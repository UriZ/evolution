import random
import math
from traits import decode_traits as decode_traits_fn

class Organism:
    def __init__(self, dna, x=0, y=0):
        self.dna = dna
        self.x = x
        self.y = y
        self.fitness = 0
        self.kills = 0
        self.alive = True
        self.animation_time = random.random() * 100  # For tentacle movement

    def decode_traits(self):
        """Convert DNA to traits using trait system"""
        return decode_traits_fn(self.dna)

    def distance_to(self, other):
        """Calculate distance to another organism"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def move_toward(self, target_x, target_y, speed):
        """Move toward target position"""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.x += (dx / dist) * speed
            self.y += (dy / dist) * speed

    def can_see(self, other):
        """Check if this organism can see another"""
        traits = self.decode_traits()
        return self.distance_to(other) <= traits['vision']

    def attack(self, other):
        """Attempt to eat another organism"""
        my_traits = self.decode_traits()
        other_traits = other.decode_traits()

        # Can only eat smaller organisms
        if my_traits['size'] <= other_traits['size']:
            return False

        # Attack succeeds if power > their size (power is composed trait)
        if my_traits['power'] > other_traits['size']:
            other.alive = False
            self.kills += 1
            return True
        return False
