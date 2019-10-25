from functions.function import Function


class Sphere(Function):
    def __init__(self):
        self.lower_limit = -100
        self.upper_limit = 100

    def fitness(self, position):
        return sum([coord ** 2 for coord in position])

    def compare_fitness(self, fitness_1, fitness_2):
        return fitness_1 < fitness_2
