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
    """Draw organism with jointed tentacles and eyes"""
    import math
    if not org.alive:
        return

    traits = org.decode_traits()
    color = (traits['r'], traits['g'], traits['b'])
    radius = int(traits['size'] / 2)
    x, y = int(org.x), int(org.y)

    # Draw jointed tentacles with animated movement
    count = traits['tentacle_count']
    length = traits['tentacle_length']
    joints = traits['tentacle_joints']
    if count > 0:
        angle_step = 2 * math.pi / count
        segment_length = length / joints
        for i in range(count):
            base_angle = i * angle_step
            curr_x, curr_y = x, y
            cumulative_angle = base_angle

            for j in range(joints):
                # Animated wave motion - each joint contributes to the wave
                wave = math.sin(org.animation_time * 0.1 + i * 0.5 + j * 0.7) * 0.5
                bend = math.cos(org.animation_time * 0.08 + i) * 0.3
                cumulative_angle += wave + bend

                next_x = curr_x + math.cos(cumulative_angle) * segment_length
                next_y = curr_y + math.sin(cumulative_angle) * segment_length
                thickness = max(1, 4 - j // 2)  # Gradual taper
                pygame.draw.line(screen, color, (int(curr_x), int(curr_y)), (int(next_x), int(next_y)), thickness)
                curr_x, curr_y = next_x, next_y

    # Draw body
    pygame.draw.circle(screen, color, (x, y), radius)

    # Draw eyes
    eye_count = traits['eye_count']
    eye_size = int(traits['eye_size'])
    if eye_count > 0:
        eye_angle_step = 2 * math.pi / eye_count
        eye_distance = radius * 0.6
        for i in range(eye_count):
            angle = i * eye_angle_step
            eye_x = x + int(math.cos(angle) * eye_distance)
            eye_y = y + int(math.sin(angle) * eye_distance)
            # White outer eye
            pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), eye_size)
            # Black pupil
            pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), max(1, eye_size // 2))

def draw_population(screen, pop):
    """Draw all organisms at their positions"""
    for org in pop.organisms:
        draw_organism(screen, org)

def draw_stats(screen, font, stats, step):
    """Draw generation stats"""
    text = font.render(
        f"Gen: {stats['generation']} | Alive: {stats['alive']} | Step: {step} | Kills: {stats['max_kills']} | Traits: {stats.get('trait_count', 0)}",
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

    pop = Population(size=50, world_w=WIDTH, world_h=HEIGHT)
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

            # Animate tentacles
            for org in pop.organisms:
                org.animation_time += 1

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
