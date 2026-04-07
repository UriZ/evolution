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
        # Fire color based on hue gene: 0=red/orange, 0.5=yellow, 1=blue
        hue = traits['fire_hue']
        if hue < 0.33:  # Red/orange fire
            fire_color = (255, int(100 + hue * 300), 0)
        elif hue < 0.66:  # Yellow fire
            fire_color = (255, 255, int((hue - 0.33) * 600))
        else:  # Blue/white fire
            fire_color = (int((1 - hue) * 600), int((1 - hue) * 600), 255)

        breath_angle = math.sin(org.animation_time * 0.2) * math.pi / 4
        end_x = x + int(math.cos(breath_angle) * fire_dist)
        end_y = y + int(math.sin(breath_angle) * fire_dist)
        pygame.draw.line(screen, fire_color, (x, y), (end_x, end_y), 3)


    # Draw tongue lash
    if traits['tongue_length'] > 5:
        tongue_color = (traits['tongue_color_r'], traits['tongue_color_g'], traits['tongue_color_b'])
        tongue_angle = math.sin(org.animation_time * 0.3) * math.pi
        tongue_len = int(traits['tongue_length'])
        end_x = x + int(math.cos(tongue_angle) * tongue_len)
        end_y = y + int(math.sin(tongue_angle) * tongue_len)
        pygame.draw.line(screen, tongue_color, (x, y), (end_x, end_y), 2)

    # Draw tentacles
    count = traits['tentacle_count']
    length = traits['tentacle_length']
    joints = traits['tentacle_joints']
    tentacle_color = (traits['tentacle_color_r'], traits['tentacle_color_g'], traits['tentacle_color_b'])
    base_thickness = int(traits['tentacle_thickness'])

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
                # Thickness tapers from base to tip
                thickness = max(1, base_thickness - int(j * base_thickness / joints))
                pygame.draw.line(screen, tentacle_color, (int(curr_x), int(curr_y)), (int(next_x), int(next_y)), thickness)
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
    eye_color = (traits['eye_color_r'], traits['eye_color_g'], traits['eye_color_b'])

    if eye_count > 0:
        eye_angle_step = 2 * math.pi / eye_count
        eye_distance = radius * 0.6
        for i in range(eye_count):
            angle = i * eye_angle_step
            eye_x = x + int(math.cos(angle) * eye_distance)
            eye_y = y + int(math.sin(angle) * eye_distance)
            # White outer, colored iris, black pupil
            pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), eye_size)
            pygame.draw.circle(screen, eye_color, (eye_x, eye_y), max(1, int(eye_size * 0.7)))
            pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), max(1, eye_size // 3))

    # Draw telekinesis aura (if present)
    if traits['telekinesis'] > 5:
        aura_radius = int(radius + traits['telekinesis'] * 0.5)
        aura_color_rgb = (traits['aura_color_r'], traits['aura_color_g'], traits['aura_color_b'])

        # Pulsing aura
        pulse = (math.sin(org.animation_time * 0.05) + 1) / 2  # 0 to 1
        alpha = int(20 + pulse * 40)  # 20-60 alpha

        alpha_surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
        aura_color = (*aura_color_rgb, alpha)
        pygame.draw.circle(alpha_surface, aura_color, (aura_radius, aura_radius), aura_radius, 3)
        screen.blit(alpha_surface, (x - aura_radius, y - aura_radius))

def draw_petri_dish(screen, center_x, center_y, radius):
    """Draw realistic petri dish with enhanced UI"""
    import math

    # Drop shadow for depth
    shadow_surface = pygame.Surface((radius * 2 + 40, radius * 2 + 40), pygame.SRCALPHA)
    for i in range(8):
        shadow_alpha = 15 - i * 2
        pygame.draw.circle(shadow_surface, (0, 0, 0, shadow_alpha),
                          (radius + 20, radius + 20), radius + 8 - i)
    screen.blit(shadow_surface, (center_x - radius - 20, center_y - radius - 20))

    # Agar nutrient medium with texture
    agar_base = (242, 237, 215)
    pygame.draw.circle(screen, agar_base, (center_x, center_y), radius)

    # Agar texture variation (slightly mottled appearance)
    texture_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(50):
        import random
        angle = random.random() * 2 * math.pi
        dist = random.random() * radius * 0.9
        x = int(radius + math.cos(angle) * dist)
        y = int(radius + math.sin(angle) * dist)
        size = random.randint(2, 5)
        alpha = random.randint(3, 8)
        pygame.draw.circle(texture_surface, (230, 225, 200, alpha), (x, y), size)
    screen.blit(texture_surface, (center_x - radius, center_y - radius))

    # Grid marks for measurement (subtle)
    grid_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(4):
        # Horizontal
        y_pos = radius + (i - 1.5) * radius // 2
        pygame.draw.line(grid_surface, (200, 195, 180, 30), (0, y_pos), (radius * 2, y_pos), 1)
        # Vertical
        x_pos = radius + (i - 1.5) * radius // 2
        pygame.draw.line(grid_surface, (200, 195, 180, 30), (x_pos, 0), (x_pos, radius * 2), 1)
    screen.blit(grid_surface, (center_x - radius, center_y - radius))

    # Glass dish rim with depth
    pygame.draw.circle(screen, (120, 120, 125), (center_x, center_y), radius + 8, 3)
    pygame.draw.circle(screen, (90, 90, 95), (center_x, center_y), radius + 4, 2)
    pygame.draw.circle(screen, (70, 70, 75), (center_x, center_y), radius, 4)

    # Inner glass edge highlight
    pygame.draw.circle(screen, (180, 180, 185), (center_x, center_y), radius - 2, 1)

    # Glass reflection/shine
    reflection_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(6):
        alpha = 50 - i * 7
        pygame.draw.arc(reflection_surface, (255, 255, 255, alpha),
                       (-15, -15, radius * 2 + 30, radius * 2 + 30),
                       3.2, 6.0, 8 - i)
    screen.blit(reflection_surface, (center_x - radius, center_y - radius))

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

        screen.fill((35, 35, 38))  # Lab table background
        
        # Draw petri dish
        draw_petri_dish(screen, pop.world.center_x, pop.world.center_y, pop.world.radius)
        
        draw_population(screen, pop)
        draw_stats(screen, font, pop.stats(), step)
        pygame.display.flip()

        if not paused:
            clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
