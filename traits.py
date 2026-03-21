"""Compositional trait system with random trait generation"""
import random
import math

# Atomic traits - directly from genes
ATOMIC_TRAITS = {
    # Body
    'size': (0, lambda g: 10 + g * 30),
    'shape': (1, lambda g: int(g * 5)),  # 0=circle, 1=square, 2=triangle, 3=pentagon, 4=star
    'r': (2, lambda g: int(g * 255)),
    'g': (3, lambda g: int(g * 255)),
    'b': (4, lambda g: int(g * 255)),

    # Tentacles
    'tentacle_count': (5, lambda g: int(g * 16)),
    'tentacle_length': (6, lambda g: 5 + g * 35),
    'tentacle_joints': (7, lambda g: int(g * 6) + 2),

    # Movement & Senses
    'speed': (8, lambda g: g * 5),  # 0-5 pixels/step
    'vision_base': (9, lambda g: 20 + g * 180),
    'aggression': (10, lambda g: g),
    'power_base': (11, lambda g: 10 + g * 40),

    # Eyes
    'eye_count': (12, lambda g: int(g * 8) + 1),
    'eye_size': (13, lambda g: 2 + g * 8),

    # Special abilities
    'camouflage': (14, lambda g: g),  # 0-1: ability to match background
    'laser_power': (15, lambda g: g * 50),  # 0-50: ranged attack damage
    'flash_rate': (16, lambda g: g * 10),  # 0-10: color flashing speed
    'tongue_length': (17, lambda g: g * 40),  # 0-40: lashing tongue reach
    'fire_power': (18, lambda g: g * 30),  # 0-30: fire breath damage
    'telekinesis': (19, lambda g: g * 100),  # 0-100: force projection range
}

# Composed traits - calculated from other traits
COMPOSED_TRAITS = {
    'tentacle_weapon': lambda t: t['tentacle_count'] * t['tentacle_length'] * t['tentacle_joints'] * 0.1,
    'melee_power': lambda t: t['power_base'] + t['tentacle_weapon'] + t['tongue_length'] * 0.5,
    'ranged_power': lambda t: t['laser_power'] + t['fire_power'] + t['telekinesis'] * 0.2,
    'power': lambda t: t['melee_power'] + t['ranged_power'],
    'eye_effectiveness': lambda t: t['eye_count'] * t['eye_size'],
    'vision': lambda t: t['vision_base'] * (1 + t['eye_effectiveness'] * 0.01),
    'stealth': lambda t: t['camouflage'] * (1 - t['flash_rate'] * 0.05),  # Flashing reduces stealth
    'intimidation': lambda t: t['flash_rate'] * t['size'] * 0.1,  # Flashing + size = scary
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
