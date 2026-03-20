import random

def random_dna(length=10):
    """Generate random DNA as array of floats [0, 1]"""
    return [random.random() for _ in range(length)]

def crossover(parent1, parent2):
    """Mix two parent DNAs to create child DNA"""
    return [random.choice([g1, g2]) for g1, g2 in zip(parent1, parent2)]

def mutate(dna, rate=0.1, amount=0.1):
    """Randomly modify genes
    rate: probability each gene mutates
    amount: max change to gene value
    """
    return [
        max(0, min(1, gene + random.uniform(-amount, amount)))
        if random.random() < rate else gene
        for gene in dna
    ]

def reproduce(parent1, parent2, mutation_rate=0.1):
    """Create offspring from two parents"""
    child = crossover(parent1, parent2)
    return mutate(child, mutation_rate)
