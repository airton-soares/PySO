import random


class Particle:
    def __init__(self, dimension, lower_limit, upper_limit):
        self.curr_position = [random.uniform(lower_limit, upper_limit) for _ in range(dimension)]
        self.best_position = self.curr_position.copy()
        self.velocity = [random.uniform(lower_limit, upper_limit) for _ in range(dimension)]
        self.dimension = dimension
