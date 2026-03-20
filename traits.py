"""Compositional trait system with random trait generation"""
import random
import math

# Atomic traits - directly from genes
ATOMIC_TRAITS = {
    'size': (0, lambda g: 10 + g * 30),
    'r': (1, lambda g: int(g * 255)),
    'g': (2, lambda g: int(g * 255)),
    'b': (3, lambda g: int(g * 255)),
    'tentacle_count': (4, lambda g: int(g * 16)),
    'tentacle_length': (5, lambda g: 5 + g * 35),
    'tentacle_joints': (6, lambda g: int(g * 6) + 2),
    'speed': (7, lambda g: g * 3),
    'vision_base': (8, lambda g: 20 + g * 180),
    'aggression': (9, lambda g: g),
    'power_base': (10, lambda g: 10 + g * 40),
    'eye_count': (11, lambda g: int(g * 8) + 1),
    'eye_size': (12, lambda g: 2 + g * 8),
}

# Composed traits - calculated from other traits
COMPOSED_TRAITS = {
    'tentacle_weapon': lambda t: t['tentacle_count'] * t['tentacle_length'] * t['tentacle_joints'] * 0.1,
    'power': lambda t: t['power_base'] + t['tentacle_weapon'],
    'eye_effectiveness': lambda t: t['eye_count'] * t['eye_size'],
    'vision': lambda t: t['vision_base'] * (1 + t['eye_effectiveness'] * 0.01),
}

def get_dna_length():
    return max(idx for idx, _ in ATOMIC_TRAITS.values()) + 1

def decode_traits(dna):
    """Decode DNA into full trait dictionary"""
    traits = {}

    # Decode atomic traits from genes
    for name, (gene_idx, decode_fn) in ATOMIC_TRAITS.items():
        traits[name] = decode_fn(dna[gene_idx])

    # Calculate composed traits
    for name, calc_fn in COMPOSED_TRAITS.items():
        traits[name] = calc_fn(traits)

    return traits

def generate_random_trait(existing_traits):
    """Generate a new random composed trait from existing traits

    Returns: (name, calculation_function) or None if generation fails
    """
    # Pick 2-3 random traits to combine
    available = [name for name in existing_traits if name not in ['r', 'g', 'b']]
    if len(available) < 2:
        return None

    components = random.sample(available, k=random.randint(2, 3))

    # Pick random combination method
    combo_type = random.choice(['multiply', 'add', 'weighted', 'max'])

    if combo_type == 'multiply':
        calc = lambda t: math.prod([t[c] for c in components])
    elif combo_type == 'add':
        calc = lambda t: sum([t[c] for c in components])
    elif combo_type == 'weighted':
        weights = [random.random() for _ in components]
        calc = lambda t: sum(t[c] * w for c, w in zip(components, weights))
    else:  # max
        calc = lambda t: max([t[c] for c in components])

    # Generate unique name
    name = f"trait_{'_'.join(components[:2])}_{combo_type}"

    return (name, calc)

def add_composed_trait(name, calc_fn):
    """Add a new composed trait"""
    COMPOSED_TRAITS[name] = calc_fn

def get_all_trait_names():
    """Get all trait names (atomic + composed)"""
    return list(ATOMIC_TRAITS.keys()) + list(COMPOSED_TRAITS.keys())
