import math
import random


def optimize(function, population, num_iterations, initial_inertia_coeff, final_inertia_coeff, cognitive_coeff,
             social_coeff):
    best_fitness_history = []
    inertia_coeff = initial_inertia_coeff
    inertia_rate = (initial_inertia_coeff - final_inertia_coeff) / num_iterations

    for i in range(num_iterations):
        update_population(population, function, inertia_coeff, cognitive_coeff, social_coeff, False)
        best_fitness_history.append(function.fitness(population.best_position))
        inertia_coeff -= inertia_rate

    return best_fitness_history


def optimize_with_clerc(function, population, num_iterations, cognitive_coeff, social_coeff):
    best_fitness_history = []
    phi = cognitive_coeff + social_coeff
    clerc_coeff = 2 * random.random() / math.fabs(2 - phi - math.sqrt(phi ** 2 - 4 * phi))

    for i in range(num_iterations):
        update_population(population, function, clerc_coeff, cognitive_coeff, social_coeff, True)
        best_fitness_history.append(function.fitness(population.best_position))

    return best_fitness_history


def update_population(population, function, inertia_or_clerc_coeff, cognitive_coeff, social_coeff, use_clerc):
    for sub_population in population.sub_populations:
        update_sub_population(sub_population, function, inertia_or_clerc_coeff, cognitive_coeff, social_coeff,
                              use_clerc)
        population_best_fitness = function.fitness(population.best_position)
        sub_population_best_fitness = function.fitness(sub_population.best_position)

        if function.compare_fitness(sub_population_best_fitness, population_best_fitness):
            population.best_position = sub_population.best_position


def update_sub_population(sub_population, function, inertia_or_clerc_coeff, cognitive_coeff, social_coeff, use_clerc):
    for particle in sub_population.particles:
        update_particle(particle, sub_population, function, inertia_or_clerc_coeff, cognitive_coeff, social_coeff,
                        use_clerc)

        sub_population_best_fitness = function.fitness(sub_population.best_position)
        particle_best_fitness = function.fitness(particle.best_position)

        if function.compare_fitness(particle_best_fitness, sub_population_best_fitness):
            sub_population.best_position = particle.best_position


def update_particle(particle, sub_population, function, inertia_or_clerc_coeff, cognitive_coeff, social_coeff,
                    use_clerc):
    for i in range(particle.dimension):
        r1 = random.random()
        r2 = random.random()
        particle_best_pos = particle.best_position[i]
        particle_curr_pos = particle.curr_position[i]
        particle_velocity = particle.velocity[i]
        sub_pop_best_pos = sub_population.best_position[i]

        cognitive_part = cognitive_coeff * r1 * (particle_best_pos - particle_curr_pos)
        social_part = social_coeff * r2 * (sub_pop_best_pos - particle_curr_pos)

        if use_clerc:
            new_velocity = inertia_or_clerc_coeff * (particle_velocity + cognitive_part + social_part)
        else:
            new_velocity = inertia_or_clerc_coeff * particle_velocity + cognitive_part + social_part

        new_position = particle_curr_pos + new_velocity

        particle.curr_position[i] = update_attributes(new_position, function.lower_limit, function.upper_limit)
        particle.velocity[i] = update_attributes(new_velocity, function.lower_limit / 5, function.upper_limit / 5)

    particle_curr_pos_fitness = function.fitness(particle.curr_position)
    particle_best_pos_fitness = function.fitness(particle.best_position)

    if function.compare_fitness(particle_curr_pos_fitness, particle_best_pos_fitness):
        particle.best_position = particle.curr_position.copy()


def update_attributes(new_value, lower_limit, upper_limit):
    if new_value > upper_limit:
        return upper_limit
    elif new_value < lower_limit:
        return lower_limit
    else:
        return new_value
