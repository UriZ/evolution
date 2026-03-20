import random
from genetics import random_dna, reproduce
from organism import Organism
from traits import get_dna_length, generate_random_trait, add_composed_trait, get_all_trait_names

class Population:
    def __init__(self, size=100, world_w=800, world_h=600):
        self.world_w = world_w
        self.world_h = world_h
        dna_length = get_dna_length()
        self.organisms = [
            Organism(random_dna(dna_length),
                     random.randint(0, world_w),
                     random.randint(0, world_h))
            for _ in range(size)
        ]
        self.generation = 0
        self.initial_size = size
        self.fitness_history = []
        self.last_trait_gen = 0

    def simulate_step(self):
        """One step of movement and predator-prey interactions"""
        alive = [o for o in self.organisms if o.alive]

        for org in alive:
            traits = org.decode_traits()

            # Find nearest prey (smaller organisms in vision range)
            prey_in_range = [
                other for other in alive
                if other != org and other.alive
                and org.can_see(other)
                and traits['size'] > other.decode_traits()['size']
            ]

            if prey_in_range and random.random() < traits['aggression']:
                # Chase nearest prey
                nearest = min(prey_in_range, key=lambda p: org.distance_to(p))
                org.move_toward(nearest.x, nearest.y, traits['speed'])

                # Try to attack if close enough
                if org.distance_to(nearest) < traits['size']:
                    org.attack(nearest)
            else:
                # Random movement
                org.x += random.uniform(-traits['speed'], traits['speed'])
                org.y += random.uniform(-traits['speed'], traits['speed'])

            # Keep in bounds
            org.x = max(0, min(self.world_w, org.x))
            org.y = max(0, min(self.world_h, org.y))

    def evaluate(self, fitness_fn):
        """Evaluate fitness for all organisms"""
        for org in self.organisms:
            fitness_fn(org)

    def select_parent(self):
        """Tournament selection: pick best of 3 random organisms"""
        alive = [o for o in self.organisms if o.alive]
        if len(alive) < 3:
            return random.choice(alive) if alive else self.organisms[0]
        tournament = random.sample(alive, 3)
        return max(tournament, key=lambda o: o.fitness)

    def is_fitness_plateau(self, window=10, threshold=5):
        """Check if fitness has plateaued"""
        if len(self.fitness_history) < window:
            return False

        recent = self.fitness_history[-window:]
        max_recent = max(recent)
        min_recent = min(recent)
        return (max_recent - min_recent) < threshold

    def try_generate_trait(self):
        """Try to generate a new random trait"""
        result = generate_random_trait(get_all_trait_names())
        if result:
            name, calc_fn = result
            add_composed_trait(name, calc_fn)
            return name
        return None

    def evolve(self, mutation_rate=0.1, trait_gen_interval=20):
        """Create next generation from survivors"""
        # Track fitness
        alive = [o for o in self.organisms if o.alive]
        if alive:
            max_fitness = max(o.fitness for o in alive)
            self.fitness_history.append(max_fitness)

        # Generate new trait if plateau or interval reached
        gens_since_trait = self.generation - self.last_trait_gen
        if gens_since_trait >= trait_gen_interval or self.is_fitness_plateau():
            new_trait = self.try_generate_trait()
            if new_trait:
                self.last_trait_gen = self.generation

        # Create new generation
        new_organisms = []
        dna_length = get_dna_length()
        for _ in range(self.initial_size):
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            child_dna = reproduce(parent1.dna, parent2.dna, mutation_rate)
            new_organisms.append(
                Organism(child_dna,
                         random.randint(0, self.world_w),
                         random.randint(0, self.world_h))
            )

        self.organisms = new_organisms
        self.generation += 1

    def stats(self):
        """Return population statistics"""
        alive = [o for o in self.organisms if o.alive]
        if not alive:
            return {
                'generation': self.generation,
                'alive': 0,
                'avg_kills': 0,
                'max_kills': 0,
                'trait_count': len(get_all_trait_names()),
            }

        kills = [o.kills for o in alive]
        return {
            'generation': self.generation,
            'alive': len(alive),
            'avg_kills': sum(kills) / len(kills),
            'max_kills': max(kills),
            'trait_count': len(get_all_trait_names()),
        }
