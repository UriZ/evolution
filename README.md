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

- 100 organisms with colored bodies and tentacles
- Evolution toward target: blue, fast, 8 long tentacles
- Fitness stats shown in top-left
- ~5 generations per second

## Current Traits (7 genes)

- Body size (10-40 pixels)
- Body color (RGB)
- Tentacle count (0-8)
- Tentacle length (5-30 pixels)
- Speed (0-10 units/step)

## Implementation Status

- ✅ Phase 1: Genetics engine (DNA, crossover, mutation, selection)
- ✅ Phase 2: Simple visualization (colored circles, grid layout)
- ✅ Phase 3: Tentacles (count, length - partial)
- ⬜ Phase 3 remaining: Shapes
- ⬜ Phase 4: Movement/animation
- ⬜ Phase 5: Interactivity

## Files

- `genetics.py` - DNA operations (crossover, mutation)
- `organism.py` - Trait decoding and fitness evaluation
- `population.py` - Selection and evolution
- `test_evolution.py` - Command-line test (verify evolution works)
- `visualize.py` - pygame visualization
