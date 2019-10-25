from models.particle import Particle
from models.sub_population import SubPopulation
from models.topology_type import TopologyType


class Population:
    def __init__(self, population_size, dimension, lower_limit, upper_limit, topology_type):
        particles = [Particle(dimension, lower_limit, upper_limit) for _ in range(population_size)]
        self.best_position = particles[0].best_position

        if topology_type == TopologyType.GLOBAL.value:
            self.sub_populations = [SubPopulation(particles)]
        elif topology_type == TopologyType.RING.value:
            self.sub_populations = []

            for i in range(population_size):
                sub_pop_particles = [particles[i]]

                if i < population_size - 1:
                    sub_pop_particles.append(particles[i + 1])
                else:
                    sub_pop_particles.append(particles[0])

                self.sub_populations.append(SubPopulation(sub_pop_particles))
        elif topology_type == TopologyType.FOCAL.value:
            self.sub_populations = []
            center = particles[0]

            for i in range(1, population_size):
                sub_pop_particles = [center, particles[i]]
                self.sub_populations.append(SubPopulation(sub_pop_particles))
