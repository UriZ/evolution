#!/usr/bin/env python3
"""Phase 2: Simple visualization of evolution"""

import pygame
import sys
from population import Population

# Config
WIDTH, HEIGHT = 800, 600
GRID_COLS = 10
GRID_ROWS = 10
TARGET = {'size': 35, 'r': 255, 'g': 50, 'b': 50}

def fitness_fn(organism):
    organism.evaluate_fitness(TARGET)

def draw_organism(screen, org, x, y):
    """Draw organism as circle"""
    traits = org.decode_traits()
    color = (traits['r'], traits['g'], traits['b'])
    radius = int(traits['size'] / 2)
    pygame.draw.circle(screen, color, (x, y), radius)

def draw_population(screen, pop):
    """Draw all organisms in grid layout"""
    cell_w = WIDTH // GRID_COLS
    cell_h = HEIGHT // GRID_ROWS

    for i, org in enumerate(pop.organisms[:GRID_COLS * GRID_ROWS]):
        row = i // GRID_COLS
        col = i % GRID_COLS
        x = col * cell_w + cell_w // 2
        y = row * cell_h + cell_h // 2
        draw_organism(screen, org, x, y)

def draw_stats(screen, font, stats):
    """Draw generation stats"""
    text = font.render(
        f"Gen: {stats['generation']} | Avg: {stats['avg_fitness']:.1f} | Max: {stats['max_fitness']:.1f}",
        True, (255, 255, 255)
    )
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, text.get_width() + 10, text.get_height() + 10))
    screen.blit(text, (5, 5))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Evolution Simulator")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()

    pop = Population(size=100, dna_length=4)
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            pop.evaluate(fitness_fn)

        screen.fill((40, 40, 40))
        draw_population(screen, pop)
        draw_stats(screen, font, pop.stats())
        pygame.display.flip()

        if not paused:
            pop.evolve(mutation_rate=0.1)
            clock.tick(5)  # 5 generations per second

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
