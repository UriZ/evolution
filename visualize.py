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
    """Draw organism with shape, tentacles, eyes, and special abilities"""
    import math
    if not org.alive:
        return

    traits = org.decode_traits()

    # Apply flashing color effect (dramatic pulse)
    if traits['flash_rate'] > 1:
        flash = (math.sin(org.animation_time * traits['flash_rate'] * 0.05) + 1) / 2  # 0 to 1
        # Alternate between base color and inverted/bright color
        color = (
            int(traits['r'] * (0.3 + flash * 0.7)),
            int(traits['g'] * (0.3 + flash * 0.7)),
            int(traits['b'] * (0.3 + flash * 0.7))
        )
    else:
        color = (traits['r'], traits['g'], traits['b'])

    radius = int(traits['size'] / 2)
    x, y = int(org.x), int(org.y)

    # Draw fire breath (if organism has fire power)
    if traits['fire_power'] > 5:
        fire_dist = int(traits['fire_power'])
        fire_color = (255, min(200, int(traits['fire_power'] * 4)), 0)
        breath_angle = math.sin(org.animation_time * 0.2) * math.pi / 4
        end_x = x + int(math.cos(breath_angle) * fire_dist)
        end_y = y + int(math.sin(breath_angle) * fire_dist)
        pygame.draw.line(screen, fire_color, (x, y), (end_x, end_y), 3)


    # Draw tongue lash
    if traits['tongue_length'] > 5:
        tongue_angle = math.sin(org.animation_time * 0.3) * math.pi
        tongue_len = int(traits['tongue_length'])
        end_x = x + int(math.cos(tongue_angle) * tongue_len)
        end_y = y + int(math.sin(tongue_angle) * tongue_len)
        pygame.draw.line(screen, (255, 100, 150), (x, y), (end_x, end_y), 2)

    # Draw tentacles
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
                wave = math.sin(org.animation_time * 0.1 + i * 0.5 + j * 0.7) * 0.5
                bend = math.cos(org.animation_time * 0.08 + i) * 0.3
                cumulative_angle += wave + bend

                next_x = curr_x + math.cos(cumulative_angle) * segment_length
                next_y = curr_y + math.sin(cumulative_angle) * segment_length
                thickness = max(1, 4 - j // 2)
                pygame.draw.line(screen, color, (int(curr_x), int(curr_y)), (int(next_x), int(next_y)), thickness)
                curr_x, curr_y = next_x, next_y

    # Draw body shape
    shape = traits['shape']
    if shape == 0:  # Circle
        pygame.draw.circle(screen, color, (x, y), radius)
    elif shape == 1:  # Square
        rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        pygame.draw.rect(screen, color, rect)
    elif shape == 2:  # Triangle
        points = [
            (x, y - radius),
            (x - radius, y + radius),
            (x + radius, y + radius)
        ]
        pygame.draw.polygon(screen, color, points)
    elif shape == 3:  # Pentagon
        points = [(x + radius * math.cos(i * 2 * math.pi / 5 - math.pi/2),
                   y + radius * math.sin(i * 2 * math.pi / 5 - math.pi/2)) for i in range(5)]
        pygame.draw.polygon(screen, color, points)
    else:  # Star
        points = []
        for i in range(10):
            r = radius if i % 2 == 0 else radius // 2
            angle = i * math.pi / 5 - math.pi/2
            points.append((x + r * math.cos(angle), y + r * math.sin(angle)))
        pygame.draw.polygon(screen, color, points)

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
            pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), eye_size)
            pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), max(1, eye_size // 2))

    # Draw telekinesis aura (if powerful)
    if traits['telekinesis'] > 20:
        aura_radius = int(radius + traits['telekinesis'] * 0.3)
        alpha_surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
        aura_color = (*color, 30)
        pygame.draw.circle(alpha_surface, aura_color, (aura_radius, aura_radius), aura_radius)
        screen.blit(alpha_surface, (x - aura_radius, y - aura_radius))

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
                pop.evolve(mutation_rate=0.1, trait_gen_interval=5)  # Generate traits every 5 gens for testing
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
