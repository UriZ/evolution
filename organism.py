import random
import math

class Organism:
    def __init__(self, dna, x=0, y=0):
        self.dna = dna
        self.x = x
        self.y = y
        self.fitness = 0
        self.kills = 0
        self.alive = True

    def decode_traits(self):
        """Convert DNA to traits"""
        return {
            'size': 10 + self.dna[0] * 30,  # 10-40 pixels
            'r': int(self.dna[1] * 255),
            'g': int(self.dna[2] * 255),
            'b': int(self.dna[3] * 255),
            'tentacle_count': int(self.dna[4] * 16),  # 0-16 tentacles
            'tentacle_length': 5 + self.dna[5] * 35,  # 5-40 pixels
            'speed': self.dna[6] * 3,  # 0-3 pixels/step
            'vision': 20 + self.dna[7] * 180,  # 20-200 pixel range
            'aggression': self.dna[8],  # 0-1 (attack probability)
            'power': 10 + self.dna[9] * 40,  # 10-50 attack power
            'eye_count': int(self.dna[10] * 8) + 1,  # 1-8 eyes
            'eye_size': 2 + self.dna[11] * 8,  # 2-10 pixel radius
            'tentacle_joints': int(self.dna[12] * 3) + 1,  # 1-3 joints
        }

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

        # Attack succeeds if power > their size
        if my_traits['power'] > other_traits['size']:
            other.alive = False
            self.kills += 1
            return True
        return False
