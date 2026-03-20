#!/usr/bin/env python3
"""Phase 2: Simple visualization of evolution"""

import pygame
import sys
from population import Population

# Config
WIDTH, HEIGHT = 800, 600
STEPS_PER_GEN = 200  # Simulation steps before next generation

def fitness_fn(organism):
    """Fitness = survival and kills"""
    if not organism.alive:
        organism.fitness = 0
    else:
        organism.fitness = 100 + organism.kills * 50

def draw_organism(screen, org):
    """Draw organism at its position with tentacles"""
    import math
    if not org.alive:
        return

    traits = org.decode_traits()
    color = (traits['r'], traits['g'], traits['b'])
    radius = int(traits['size'] / 2)
    x, y = int(org.x), int(org.y)

    # Draw tentacles
    count = traits['tentacle_count']
    length = traits['tentacle_length']
    if count > 0:
        angle_step = 2 * math.pi / count
        for i in range(count):
            angle = i * angle_step
            end_x = x + int(math.cos(angle) * (radius + length))
            end_y = y + int(math.sin(angle) * (radius + length))
            pygame.draw.line(screen, color, (x, y), (end_x, end_y), 2)

    # Draw body
    pygame.draw.circle(screen, color, (x, y), radius)

def draw_population(screen, pop):
    """Draw all organisms at their positions"""
    for org in pop.organisms:
        draw_organism(screen, org)

def draw_stats(screen, font, stats, step):
    """Draw generation stats"""
    text = font.render(
        f"Gen: {stats['generation']} | Alive: {stats['alive']} | Step: {step} | Kills: {stats['max_kills']}",
        True, (255, 255, 255)
    )
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, text.get_width() + 10, text.get_height() + 10))
    screen.blit(text, (5, 5))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Evolution Simulator - Predator/Prey")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()

    pop = Population(size=50, dna_length=10, world_w=WIDTH, world_h=HEIGHT)
    running = True
    paused = False
    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            pop.simulate_step()
            step += 1

            # Evolve after simulation period
            if step >= STEPS_PER_GEN:
                pop.evaluate(fitness_fn)
                pop.evolve(mutation_rate=0.1)
                step = 0

        screen.fill((40, 40, 40))
        draw_population(screen, pop)
        draw_stats(screen, font, pop.stats(), step)
        pygame.display.flip()

        if not paused:
            clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
