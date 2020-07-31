import os
from argparse import ArgumentParser

import pso
import time
import matplotlib.pyplot as plt
from functions.function_factory import build_function
from functions.function_type import FunctionType
from models.population import Population
from models.topology_type import TopologyType


def build_args_parser():
    usage = 'python pyso.py -d <dimension>\n       ' \
            'run with --help for arguments descriptions'
    parser = ArgumentParser(description='A Python implementation of the Particle Swarm Optimizaion', usage=usage)

    parser.add_argument('-d', '--dimension', dest='dimension', type=int, default=30,
                        help='Dimension of the function to be optimized')
    parser.add_argument('-p', '--population', dest='population_size', type=int, default=30,
                        help='Size of the particle swarm population')
    parser.add_argument('-i', '--iterations', dest='num_iterations', type=int, default=10000,
                        help='Number of iterations in the optimization or max number of iterations without improvement'
                             'if the parameter "--rate" is bigger then 0')
    parser.add_argument('-c', '--cognitive', dest='cognitive_coeff', type=float, default=2.05,
                        help='Cognitive coefficient')
    parser.add_argument('-s', '--social', dest='social_coeff', type=float, default=2.05,
                        help='Social coefficient')
    parser.add_argument('-ii', '--initial_inertia', dest='initial_inertia_coeff', type=float, default=0.8,
                        help='Initial inertia coefficient. Decays linearly to the value in "final_inertia". If the'
                             'Clerc\'s coefficient is been used this vale will be replaced')
    parser.add_argument('-fi', '--final_inertia', dest='final_inertia_coeff', type=float, default=0.8,
                        help='Final inertia coefficient. If the Clerc\'s coefficient is been used this vale will be'
                             'replaced')
    parser.add_argument('--use_clerc', action='store_true',
                        help='Defines either the Clerc\'s coefficient will used or not')
    parser.add_argument('-sim', '--simulations', dest='num_simulations', type=int, default=30,
                        help='Number of simulations to be done for the optimization')
    parser.add_argument('-o', '--output', dest='output_path', type=str, default='results',
                        help='Output path')

    return parser


def main():
    args_parser = build_args_parser()
    args = args_parser.parse_args()

    results_dir_path = args.output_path

    if not os.path.exists(results_dir_path):
        os.makedirs(results_dir_path)

    for function_type in [f.value for f in FunctionType]:
        function = build_function(function_type)
        best_fitness_history_by_topology_type = {}

        for topology_type in [t.value for t in TopologyType]:
            best_fitness_history = []

            for i in range(args.num_simulations):
                start_time = time.time()
                
                population = Population(args.population_size, args.dimension, function.lower_limit, function.upper_limit,
                                        topology_type)
                                    
                if args.use_clerc:
                    best_fitness = pso.optimize_with_clerc(function, population, args.num_iterations,
                                                           args.cognitive_coeff, args.social_coeff)
                else:
                    best_fitness = pso.optimize(function, population, args.num_iterations,
                                                args.initial_inertia_coeff, args.final_inertia_coeff,
                                                args.cognitive_coeff, args.social_coeff)
                
                elapsed_time = time.time() - start_time
                
                print(function_type + ", " + topology_type + ", simulação: " + str(i + 1) + ", fitness: " +
                      str(round(best_fitness, 2)) + "(" + str(round(elapsed_time, 2)) + " s)")
                
                best_fitness_history.append(best_fitness)

            best_fitness_history_by_topology_type[topology_type] = best_fitness_history
        
        plt.clf()
        plt.boxplot(list(best_fitness_history_by_topology_type.values()),
                    labels=list(best_fitness_history_by_topology_type.keys()))
        plt.title(function_type)
        plt.savefig(os.path.join(results_dir_path, function_type + "_box_plot.png"), bbox_inches='tight')


if __name__ == '__main__':
    main()
