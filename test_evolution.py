#!/usr/bin/env python3
"""Test genetics engine - verify evolution works without visualization"""

from population import Population

# Target: large red organisms
TARGET = {'size': 35, 'r': 255, 'g': 0, 'b': 0}

def fitness_fn(organism):
    organism.evaluate_fitness(TARGET)

# Create population
pop = Population(size=100, dna_length=4)

# Run evolution
print("Generation | Avg Fitness | Max Fitness")
print("-" * 40)

for _ in range(50):
    pop.evaluate(fitness_fn)
    stats = pop.stats()
    print(f"{stats['generation']:10d} | {stats['avg_fitness']:11.1f} | {stats['max_fitness']:11.1f}")
    pop.evolve(mutation_rate=0.1)

# Show best organism traits
pop.evaluate(fitness_fn)
best = max(pop.organisms, key=lambda o: o.fitness)
traits = best.decode_traits()
print(f"\nBest organism traits:")
print(f"  Size: {traits['size']:.1f} (target: {TARGET['size']})")
print(f"  Color: RGB({traits['r']}, {traits['g']}, {traits['b']}) (target: RGB({TARGET['r']}, {TARGET['g']}, {TARGET['b']}))")
