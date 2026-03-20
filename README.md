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

- 100 organisms displayed as colored circles
- Colors and sizes evolve toward target (reddish, size ~35)
- Fitness stats shown in top-left
- ~5 generations per second

## Implementation Status

- ✅ Phase 1: Genetics engine (DNA, crossover, mutation, selection)
- ✅ Phase 2: Simple visualization (colored circles, grid layout)
- ⬜ Phase 3: Complex features (shapes, tentacles)
- ⬜ Phase 4: Movement/animation
- ⬜ Phase 5: Interactivity

## Files

- `genetics.py` - DNA operations (crossover, mutation)
- `organism.py` - Trait decoding and fitness evaluation
- `population.py` - Selection and evolution
- `test_evolution.py` - Command-line test (verify evolution works)
- `visualize.py` - pygame visualization
