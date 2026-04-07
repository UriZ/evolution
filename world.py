"""World/environment management for evolution simulator"""
import math
import random


class PetriDish:
    """Circular petri dish environment with boundary enforcement"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = min(width, height) // 2 - 20
    
    def random_position(self):
        """Generate a random position within the dish"""
        angle = random.random() * 2 * math.pi
        distance = random.random() * self.radius * 0.9  # Keep away from edge
        x = self.center_x + distance * math.cos(angle)
        y = self.center_y + distance * math.sin(angle)
        return x, y
    
    def enforce_bounds(self, organism):
        """Keep organism within circular boundary"""
        dx = organism.x - self.center_x
        dy = organism.y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > self.radius:
            # Push back to edge
            angle = math.atan2(dy, dx)
            organism.x = self.center_x + self.radius * math.cos(angle)
            organism.y = self.center_y + self.radius * math.sin(angle)
