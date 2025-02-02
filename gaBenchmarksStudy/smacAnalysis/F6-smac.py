#!/usr/bin/python
import sys
import array
import random
from deap import base
from deap import creator
from deap import tools
import fgeneric
import numpy as np
from operator import attrgetter

import bbobbenchmarks as bn

toolbox = base.Toolbox()
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode="d",
               fitness=creator.FitnessMin)
# pool = multiprocessing.Pool()
# toolbox.register("map", futures.map)


def tupleize(func):
    """A decorator that tuple-ize the result of a function. This is useful
    when the evaluation function returns a single value.
    """
    def wrapper(*args, **kargs):
        return func(*args, **kargs),
    return wrapper


def main(func,
         NGEN,
         CXPB,
         MUTPB,
         dim,
         ftarget,
         tournsize,
         n_aval,
         eta,
         sigma,
         mu,
         indp
         ):
    toolbox.register("attr_float", random.random)
    toolbox.register("select", tools.selTournament, tournsize=tournsize)
    toolbox.register(
        "mutate",
        tools.mutGaussian,
        mu=mu,
        sigma=sigma,
        indpb=indp
    )
    # mutShuffleIndexes
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    # calculating the number of individuals of the
    # populations based on the number of executions
    y = int(n_aval / NGEN)
    x = n_aval - y * NGEN
    n = x + y

    toolbox.register("evaluate", func)
    toolbox.decorate("evaluate", tupleize)
    toolbox.register("attr_float", random.uniform, -5, 5)
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, eta = eta, low= -5, up = 5)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, dim)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    logbook = tools.Logbook()
    logbook.header = "gen", "min", "avg", "max", "std"
    pop = toolbox.population(n)
    # Evaluate the entire population
    # 2 model.bins: real data, generated model
    fitnesses = list(toolbox.map(toolbox.evaluate, pop))
    # numero_avaliacoes = len(pop)
    # normalize fitnesses
    # fitnesses = normalizeFitness(fitnesses)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # create offspring
        offspring = list(toolbox.map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(toolbox.map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        # The population is entirely replaced by the offspring,
        # but the last ind replaced by best_pop
        # Elitism
        best_pop = tools.selBest(pop, 1)[0]
        offspring = sorted(offspring, key=attrgetter("fitness"))
        offspring[0] = best_pop
        random.shuffle(offspring)
        pop[:] = offspring
        record = stats.compile(pop)
        logbook.record(gen=g, **record)
    return logbook, best_pop


if __name__ == "__main__":
    keys = ['key', 'NGEN', 'n_aval', 'dim']
    params = dict()
    for i in range(len(sys.argv) - 1):
        if (sys.argv[i] == '-params'):
            gaParams = sys.argv[i + 1]
        elif (sys.argv[i] == '-tournsize'):
            tournsize = int(sys.argv[i + 1])
        elif (sys.argv[i] == '-CXPB'):
            params['CXPB'] = float(sys.argv[i + 1])
        elif (sys.argv[i] == '-MUTPB'):
            params['MUTPB'] = float(sys.argv[i + 1])
        elif (sys.argv[i] == '-eta'):
            eta = float(sys.argv[i + 1])
        elif (sys.argv[i] == '-mu'):
            mu = float(sys.argv[i + 1])
        elif (sys.argv[i] == '-sigma'):
            sigma = float(sys.argv[i + 1])
        elif (sys.argv[i] == '-indp'):
            indp = float(sys.argv[i + 1])
    
    f = open(gaParams, "r")
    
    for line in f:
        if line[0] == '#':
            continue
        tokens = line.split()
        for key, value in zip(keys, tokens):
            if key == 'key':
                params[key] = value
            elif key == 'CXPB' or key == 'MUTPB':
                params[key] = float(value)
            else:
                params[key] = int(value)
    f.close()
    # Maximum number of restart for an algorithm that detects stagnation

    # Create a COCO experiment that will log the results under the
    # ./output directory
    e = fgeneric.LoggingFunction('output')

    # Iterate over all desired test dimensions
    # for dim in (2, 3, 5, 10, 20, 40):
    dim = params['dim']
    # Set the maximum number function evaluation granted to the algorithm
    # This is usually function of the dimensionality of the problem

    # Iterate over a set of benchmarks (noise free benchmarks here)
    # for f_name in bn.nfreeIDs:
    f_name = 6
    # Iterate over all the instance of a single problem
    # Rotation, translation, etc.
    # for instance in chain(range(1, 6), range(21, 31)):
    instance = 1
    # Set the function to be used (problem) in the logger
    e.setfun(*bn.instantiate(f_name, iinstance=1))

    # Independent restarts until maxfunevals or ftarget is reached
    # Run the algorithm with the remaining
    # number of evaluations
    # random.seed(params['seed'])
    logbook, best_pop = main(e.evalfun,
                   NGEN=params['NGEN'],
                   CXPB=params['CXPB'],
                   MUTPB=params['MUTPB'],
                   dim=dim,
                   n_aval=params['n_aval'],
                   tournsize=tournsize,
                   ftarget=e.ftarget,
                   eta=eta,
                   sigma=sigma,
                   mu=mu,
                   indp=indp
                 )



    # SMAC has a few different output fields; here, we only need the 4th output:
    print "Result for SMAC: SUCCESS, 0, 0, %f, 0" % best_pop.fitness.values