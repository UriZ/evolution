# Evolution Simulator

Genetic algorithm demonstrating natural selection through visual organisms.

## Quick Start

```bash
# Test genetics engine (no visualization)
./venv/bin/python test_evolution.py

# Run visual simulator
./run.sh
```

## Controls

- **Space**: Pause/resume evolution

## What You'll See

- 50 organisms moving freely, hunting each other
- Larger organisms hunt smaller ones
- Predators chase prey in vision range
- Population evolves toward apex predators
- 200 simulation steps per generation
- Stats: generation, alive count, step, max kills

## Current Traits (10 genes)

- Body size (10-40 pixels) - larger can eat smaller
- Body color (RGB)
- Tentacle count (0-8)
- Tentacle length (5-30 pixels)
- Speed (0-3 pixels/step) - chase/escape
- Vision (20-200 pixels) - detect prey/predators
- Aggression (0-1) - attack probability
- Power (10-50) - attack strength

## Implementation Status

- ✅ Phase 1: Genetics engine (DNA, crossover, mutation, selection)
- ✅ Phase 2: Simple visualization (colored circles, grid layout)
- ✅ Phase 3: Tentacles (count, length)
- ✅ Phase 4: Movement and predator-prey dynamics
- ⬜ Phase 5: Advanced interactivity

## Fitness Function

Organisms earn fitness through survival and predation:
- Dead organisms: 0 fitness
- Survivors: 100 + (50 × kills)

This drives evolution toward effective predators with:
- Good vision (find prey)
- High speed (chase/escape)
- Large size (eat more prey)
- High power (successful attacks)
- Optimal aggression (hunt but don't waste energy)

## Files

- `genetics.py` - DNA operations (crossover, mutation)
- `organism.py` - Trait decoding and fitness evaluation
- `population.py` - Selection and evolution
- `test_evolution.py` - Command-line test (verify evolution works)
- `visualize.py` - pygame visualization
