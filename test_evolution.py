#!/usr/bin/env python3
"""Test genetics engine - verify evolution works without visualization"""

from population import Population

# Target: blue organisms with many long tentacles
TARGET = {
    'r': 50, 'g': 100, 'b': 255,
    'tentacle_count': 8,
    'tentacle_length': 25,
    'speed': 7,
}

def fitness_fn(organism):
    organism.evaluate_fitness(TARGET)

# Create population
pop = Population(size=100, dna_length=7)

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
print(f"  Size: {traits['size']:.1f}")
print(f"  Color: RGB({traits['r']}, {traits['g']}, {traits['b']}) (target: RGB({TARGET['r']}, {TARGET['g']}, {TARGET['b']}))")
print(f"  Tentacles: {traits['tentacle_count']} (target: {TARGET['tentacle_count']})")
print(f"  Tentacle length: {traits['tentacle_length']:.1f} (target: {TARGET['tentacle_length']})")
print(f"  Speed: {traits['speed']:.1f} (target: {TARGET['speed']})")
