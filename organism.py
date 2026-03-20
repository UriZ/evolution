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
        }

    def evaluate_fitness(self, target):
        """Fitness = how close to target traits
        target: dict with 'size', 'r', 'g', 'b'
        """
        traits = self.decode_traits()

        size_diff = abs(traits['size'] - target['size'])
        color_diff = (
            abs(traits['r'] - target['r']) +
            abs(traits['g'] - target['g']) +
            abs(traits['b'] - target['b'])
        )

        # Lower difference = higher fitness
        self.fitness = 1000 - size_diff - color_diff
        return self.fitness
