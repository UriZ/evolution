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

    def can_attack_ranged(self, other):
        """Check if organism can attack at range"""
        my_traits = self.decode_traits()
        dist = self.distance_to(other)

        # Check ranged abilities
        max_range = max(
            my_traits['laser_power'] * 2,
            my_traits['fire_power'],
            my_traits['telekinesis']
        )

        return dist <= max_range and my_traits['ranged_power'] > 10

    def attack(self, other):
        """Attempt to eat another organism (melee or ranged)"""
        my_traits = self.decode_traits()
        other_traits = other.decode_traits()

        dist = self.distance_to(other)

        # Ranged attack
        if dist > my_traits['size'] and self.can_attack_ranged(other):
            # Stealth reduces chance of being detected/hit
            hit_chance = 0.3 * (1 - other_traits['stealth'])
            if random.random() < hit_chance and my_traits['ranged_power'] > other_traits['size'] * 0.7:
                other.alive = False
                self.kills += 1
                return True
            return False

        # Melee attack (close range)
        if dist <= my_traits['size']:
            # Can only eat smaller organisms in melee
            if my_traits['size'] <= other_traits['size']:
                return False

            if my_traits['melee_power'] > other_traits['size']:
                other.alive = False
                self.kills += 1
                return True

        return False
