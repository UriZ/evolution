# Evolution Simulator

Genetic algorithm simulation demonstrating natural selection through iterative generations.

See [INSTRUCTIONS.md](INSTRUCTIONS.md) for implementation guidelines and [design.md](design.md) for detailed design.

## Core Mechanics

- **Population**: Organisms with DNA-encoded traits
- **Reproduction**: Genetic crossover (mixing alleles) + mutations
- **Selection**: Fitness function determines survival/reproduction probability
- **Iteration**: Each generation creates offspring from fittest parents

## Goals

- Observable evolution of traits over generations
- Configurable fitness landscapes
- Real-time visual representation of population dynamics
- Demonstrate emergence of optimization without explicit design

## Constraints

- Keep genetics model simple but extensible
- Prioritize clarity of evolutionary dynamics over biological accuracy
- Performance: support populations of 100-1000+ organisms
