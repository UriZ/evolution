# Design Approach

See [INSTRUCTIONS.md](INSTRUCTIONS.md) for implementation guidelines.

## How DNA Works

### DNA = Array of Numbers
Each gene is a value between 0 and 1 that controls one aspect of the organism:

```
DNA: [0.3, 0.7, 0.5, 0.8, 0.2, 0.6, 0.4, 0.9, ...]
      │    │    │    │    │    └─ tentacle length
      │    │    │    │    └─ movement speed
      │    │    │    └─ blue color
      │    │    └─ green color
      │    └─ red color
      └─ body size/shape
```

### Gene Expression
DNA → Visual/Behavioral Traits via decoding:
- Gene 0.3 → small body
- Gene 0.9 → fast movement
- Genes [0.7, 0.5, 0.8] → purple-ish color

**Key**: Identical DNA always produces identical organism

### Reproduction

**Crossover**: Mix parent DNAs
```
Parent A: [0.3, 0.7, 0.5, 0.8, 0.2]
Parent B: [0.6, 0.2, 0.9, 0.1, 0.7]
          ↓ random mixing
Child:    [0.3, 0.2, 0.9, 0.8, 0.7]
```

**Mutation**: Random small changes
```
Before: [0.3, 0.7, 0.5]
After:  [0.3, 0.8, 0.5]  ← gene 1 mutated slightly
```

### Evolution Loop
1. Random starting population (random DNA)
2. Evaluate which organisms are "better" (fitness)
3. Better organisms more likely to reproduce
4. Create next generation from selected parents (crossover + mutation)
5. Repeat → traits shift toward "better" values

## Organism Features

### Body
- **Size**: Gene determines radius/diameter
- **Shape**: Gene picks from circle, square, triangle, pentagon, etc.
- **Color**: 3 genes (RGB) define body color
- **Pattern**: Solid, striped, spotted, gradient

### Tentacles
- **Count**: Gene determines 0-8 tentacles
- **Length**: Gene controls how far they extend from body
- **Thickness**: Gene for tentacle width
- **Angle/distribution**: Evenly spaced vs clustered
- **Color**: Inherit body color or have independent gene

### Movement
- **Speed**: Gene controls units per step
- **Direction**: Random, toward target, or gene-controlled preference
- **Pattern**: Straight, wobbly, circular

### Possible Extensions
- Eyes (count, size, position)
- Mouth/features
- Texture
- Glow/transparency
- Symmetry vs asymmetry

**Start with**: Shape, color (RGB), size, speed, tentacle count, tentacle length (~8-10 genes)

## Fitness Functions (Selection Pressure)

Fitness determines which organisms reproduce. Different functions drive different evolutionary outcomes:

### Environmental Selection
**Target Environment**: Evolve toward specific appearance
- "Evolve to be red and large"
- "Evolve to have many long tentacles"
- "Evolve to be fast and small"

### Spatial Selection
**Position-based**: Organisms closer to target location survive better
- Could drive evolution of speed (to reach target faster)
- Or specific colors associated with locations

### Resource Competition
**Scarcity model**: Limited "food" resources
- Fast organisms reach resources first
- Size might affect resource needs
- Drives speed/efficiency evolution

### Predator Avoidance
**Camouflage**: Blend into background
- Background color = target color
- Drives color evolution specifically

### User Preference
**Interactive**: User clicks preferred organisms
- Drives evolution toward aesthetic appeal
- No predetermined fitness function

**Recommendation**: Start with simple environmental target (e.g., "be large and red"), then add complexity

## Visualization

### Main Display
World space where organisms exist and are visible:
- Each organism drawn with its current traits
- Positioned in 2D space
- Can move or stay static

### What You See Evolve
- Colors shifting across generations
- Size distributions changing
- Tentacle counts increasing/decreasing
- Speed variations (if animated)
- Shape preferences emerging

### Display Modes

**Static Snapshots**: Each generation frozen, advance manually or on timer
- Clear comparison between generations
- Easy to observe changes

**Continuous Animation**: Organisms move around
- More dynamic and engaging
- Harder to track individual changes

**Side-by-Side**: Generation N vs Generation N+10
- Direct visual comparison
- Shows evolutionary trajectory

**Recommendation**: Start static, add animation later

### Stats Overlay
- Generation number
- Average fitness
- Best fitness
- Population diversity metrics
- Trait distributions (histograms/graphs)

## Architecture Overview

### Core Components

**Genome System**
- DNA representation
- Crossover logic
- Mutation logic

**Organism System**
- DNA → trait decoding
- Visual representation data
- Fitness evaluation

**Population Management**
- Collection of organisms
- Selection algorithms (tournament, roulette, etc.)
- Generation replacement strategies

**Rendering System**
- Draw individual organisms
- Update display per generation
- Handle user interaction

**Simulation Loop**
- Initialize population
- Evaluate fitness
- Select parents
- Create offspring
- Update display
- Repeat

### Data Flow

```
Random DNA → Organisms → Display
     ↓
Fitness Evaluation
     ↓
Parent Selection
     ↓
Crossover + Mutation → New DNA
     ↓
New Generation → Update Display
     ↓
(Loop back)
```

## Key Design Questions

### DNA Length
- More genes = more complexity and variation
- Fewer genes = easier to see patterns
- **Tradeoff**: Start with 8-12 genes, expand if needed

### Population Size
- Larger = smoother evolution, more visual variety
- Smaller = faster computation, easier to track individuals
- **Tradeoff**: 100-300 organisms

### Selection Pressure
- Strong = rapid evolution but premature convergence
- Weak = slow evolution, maintains diversity longer
- **Tunable parameter**: Make adjustable

### Mutation Rate
- High = exploration, prevents stagnation
- Low = refinement, stable traits
- **Tunable parameter**: Make adjustable

### Reproduction Model
- Sexual (2 parents) = complex mixing
- Asexual (1 parent + mutation) = simpler, less variation
- **Recommendation**: Sexual reproduction for richer dynamics

## Implementation Strategy

### Phase 1: Genetics Engine
- DNA operations (crossover, mutation)
- Basic trait decoding
- Population selection
- Verify evolution without visualization (print stats)

### Phase 2: Simple Visualization
- Draw organisms as circles (ignore shape gene initially)
- Show color evolution
- Static snapshots per generation

### Phase 3: Complex Features
- Add shape rendering
- Add tentacles
- Verify genes control appearance correctly

### Phase 4: Movement
- Animate organisms moving
- Speed gene affects movement
- Real-time evolution display

### Phase 5: Interactivity
- Pause/resume
- Adjust parameters (mutation, selection)
- Change fitness function
- Manual selection (click to choose parents)

## Technical Considerations

### Performance
- Rendering 200+ organisms each frame can be slow
- **Strategy**: Optimize drawing, update less frequently, or reduce population

### Emergent Complexity
- Multiple genes can interact unexpectedly
- **Strategy**: Test each trait independently first

### Visual Clarity
- Too many features = visual noise
- **Strategy**: Clear color palette, size limits, transparency

### Convergence Issues
- Population may lose diversity quickly
- **Strategy**: Diversity preservation techniques, higher mutation

## Success Criteria

You know it's working when:
1. Average fitness increases over generations
2. Visual appearance shifts toward fitness target
3. Diversity decreases over time (convergence)
4. Similar organisms cluster together
5. Reversing fitness function causes reverse evolution
