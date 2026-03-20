import random
from genetics import random_dna, reproduce
from organism import Organism

class Population:
    def __init__(self, size=100, dna_length=10):
        self.organisms = [Organism(random_dna(dna_length)) for _ in range(size)]
        self.generation = 0

    def evaluate(self, fitness_fn):
        """Evaluate fitness for all organisms"""
        for org in self.organisms:
            fitness_fn(org)

    def select_parent(self):
        """Tournament selection: pick best of 3 random organisms"""
        tournament = random.sample(self.organisms, 3)
        return max(tournament, key=lambda o: o.fitness)

    def evolve(self, mutation_rate=0.1):
        """Create next generation"""
        new_organisms = []
        for _ in range(len(self.organisms)):
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            child_dna = reproduce(parent1.dna, parent2.dna, mutation_rate)
            new_organisms.append(Organism(child_dna))

        self.organisms = new_organisms
        self.generation += 1

    def stats(self):
        """Return population statistics"""
        fitnesses = [o.fitness for o in self.organisms]
        return {
            'generation': self.generation,
            'avg_fitness': sum(fitnesses) / len(fitnesses),
            'max_fitness': max(fitnesses),
            'min_fitness': min(fitnesses),
        }
