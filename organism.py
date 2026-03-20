class Organism:
    def __init__(self, dna):
        self.dna = dna
        self.fitness = 0

    def decode_traits(self):
        """Convert DNA to visual traits"""
        return {
            'size': 10 + self.dna[0] * 30,  # 10-40 pixels
            'r': int(self.dna[1] * 255),
            'g': int(self.dna[2] * 255),
            'b': int(self.dna[3] * 255),
            'tentacle_count': int(self.dna[4] * 8),  # 0-8 tentacles
            'tentacle_length': 5 + self.dna[5] * 25,  # 5-30 pixels
            'speed': self.dna[6] * 10,  # 0-10 units/step
        }

    def evaluate_fitness(self, target):
        """Fitness = how close to target traits
        target: dict with any combination of trait keys
        """
        traits = self.decode_traits()
        diff = 0

        for key in target:
            diff += abs(traits[key] - target[key])

        # Lower difference = higher fitness
        self.fitness = 2000 - diff
        return self.fitness
