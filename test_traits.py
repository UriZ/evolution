#!/usr/bin/env python3
"""Test trait generation"""

from traits import generate_random_trait, get_all_trait_names, add_composed_trait, decode_traits, get_dna_length
from genetics import random_dna

# Check initial state
print(f"DNA length: {get_dna_length()}")
print(f"All traits: {get_all_trait_names()}")
print(f"Trait count: {len(get_all_trait_names())}")

# Test trait generation
for i in range(5):
    result = generate_random_trait(get_all_trait_names())
    if result:
        name, calc_fn = result
        add_composed_trait(name, calc_fn)
        print(f"Generated trait {i+1}: {name}")
    else:
        print(f"Trait generation {i+1} failed")

print(f"\nFinal trait count: {len(get_all_trait_names())}")
print(f"All traits: {get_all_trait_names()}")

# Test decoding
dna = random_dna(get_dna_length())
traits = decode_traits(dna)
print(f"\nSample traits from DNA:")
for k, v in list(traits.items())[:5]:
    print(f"  {k}: {v}")
