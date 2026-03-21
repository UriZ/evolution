#!/usr/bin/env python3
"""Test that trait count updates correctly"""

from traits import get_all_trait_names, add_composed_trait

print(f"Initial trait count: {len(get_all_trait_names())}")

# Simulate adding a new trait
add_composed_trait("test_trait_1", lambda t: t['size'] + t['speed'])
print(f"After adding 1 trait: {len(get_all_trait_names())}")

add_composed_trait("test_trait_2", lambda t: t['power'] * t['vision'])
print(f"After adding 2 traits: {len(get_all_trait_names())}")

print(f"All traits: {get_all_trait_names()}")
