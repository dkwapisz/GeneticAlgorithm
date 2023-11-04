import random

import numpy as np

from algorithm.Individual import Individual, validateGen
from algorithm.Population import Population


def onePointCrossover(population, probability):
    individualAfterCross = []

    for i in range(0, len(population.individuals), 2):
        parent1 = population.individuals[i]
        parent2 = population.individuals[i + 1]

        child1Chromosome = []
        child2Chromosome = []

        if random.random() > probability:
            child1Chromosome = parent1.getChromosomeBinary()
            child2Chromosome = parent2.getChromosomeBinary()
        else:
            for variable in range(population.variableNums):
                crossPoint = np.random.randint(1, len(parent1.chromosomeBinary[variable]))
                child1Gen = np.concatenate(
                    (parent1.chromosomeBinary[variable][:crossPoint], parent2.chromosomeBinary[variable][crossPoint:]))
                child2Gen = np.concatenate(
                    (parent2.chromosomeBinary[variable][:crossPoint], parent1.chromosomeBinary[variable][crossPoint:]))
                child1Chromosome.append(child1Gen)
                child2Chromosome.append(child2Gen)

        child1 = Individual(None, child1Chromosome)
        child2 = Individual(None, child2Chromosome)

        individualAfterCross.extend([child1, child2])

    newPopulation = Population(population.variableNums)
    newPopulation.individuals = np.array(individualAfterCross)

    return newPopulation


def twoPointCrossover(population, probability):
    individualAfterCross = []

    for i in range(0, len(population.individuals), 2):
        parent1 = population.individuals[i]
        parent2 = population.individuals[i + 1]

        child1Chromosome = []
        child2Chromosome = []

        if random.random() > probability:
            child1Chromosome = parent1.getChromosomeBinary()
            child2Chromosome = parent2.getChromosomeBinary()
        else:
            for variable in range(population.variableNums):
                crossPoints = np.sort(np.random.choice(len(parent1.chromosomeBinary[variable]), 2, replace=False))
                child1Gen = np.concatenate([
                    parent1.chromosomeBinary[variable][:crossPoints[0]],
                    parent2.chromosomeBinary[variable][crossPoints[0]:crossPoints[1]],
                    parent1.chromosomeBinary[variable][crossPoints[1]:]
                ])
                child2Gen = np.concatenate([
                    parent2.chromosomeBinary[variable][:crossPoints[0]],
                    parent1.chromosomeBinary[variable][crossPoints[0]:crossPoints[1]],
                    parent2.chromosomeBinary[variable][crossPoints[1]:]
                ])
                child1Chromosome.append(child1Gen)
                child2Chromosome.append(child2Gen)

        child1 = Individual(None, child1Chromosome)
        child2 = Individual(None, child2Chromosome)

        individualAfterCross.extend([child1, child2])

    newPopulation = Population(population.variableNums)
    newPopulation.individuals = np.array(individualAfterCross)

    return newPopulation


def threePointCrossover(population: Population, probability: float) -> Population:
    new_population = Population(population.variableNums)
    individual_after_cross = []

    for i in range(0, len(population.individuals), 2):
        child1_chromosome = []
        child2_chromosome = []

        if random.random() > probability:
            for variable in range(population.variableNums):
                parent1_chromosome = population.individuals[i].getChromosomeBinary()[variable]
                parent2_chromosome = population.individuals[i + 1].getChromosomeBinary()[variable]
                child1_chromosome.append(parent1_chromosome)
                child2_chromosome.append(parent2_chromosome)
        else:
            for variable in range(population.variableNums):
                parent1 = population.individuals[i]
                parent2 = population.individuals[i + 1]
                cross_points = np.sort(np.random.choice(len(parent1.chromosomeBinary[variable]), 3, replace=False))

                child1_gen = np.concatenate((
                    parent1.chromosomeBinary[variable][:cross_points[0]],
                    parent2.chromosomeBinary[variable][cross_points[0]:cross_points[1]],
                    parent1.chromosomeBinary[variable][cross_points[1]:cross_points[2]],
                    parent2.chromosomeBinary[variable][cross_points[2]:]
                ))

                child2_gen = np.concatenate((
                    parent2.chromosomeBinary[variable][:cross_points[0]],
                    parent1.chromosomeBinary[variable][cross_points[0]:cross_points[1]],
                    parent2.chromosomeBinary[variable][cross_points[1]:cross_points[2]],
                    parent1.chromosomeBinary[variable][cross_points[2]:]
                ))

                child1_chromosome.append(child1_gen)
                child2_chromosome.append(child2_gen)

        child1 = Individual(None, child1_chromosome)
        child2 = Individual(None, child2_chromosome)
        individual_after_cross.extend([child1, child2])

    new_population.individuals = np.array(individual_after_cross)
    return new_population


def uniformCrossover(population: Population, probability: float) -> Population:
    individualAfterCross = []

    for i in range(0, len(population.individuals), 2):
        child1Chromosome = []
        child2Chromosome = []
        if random.random() > probability:
            for variable in range(population.variableNums):
                child1Chromosome.append(population.individuals[i].getChromosomeBinary()[variable])
                child2Chromosome.append(population.individuals[i + 1].getChromosomeBinary()[variable])
        else:
            for variable in range(population.variableNums):
                parent1 = population.individuals[i]
                parent2 = population.individuals[i + 1]

                child1Gen = np.empty_like(parent1.chromosomeBinary[variable])
                child2Gen = np.empty_like(parent2.chromosomeBinary[variable])

                for j in range(len(parent1.chromosomeBinary[variable])):
                    if np.random.rand() < probability:
                        child1Gen[j] = parent1.chromosomeBinary[variable][j]
                        child2Gen[j] = parent2.chromosomeBinary[variable][j]
                    else:
                        child1Gen[j] = parent2.chromosomeBinary[variable][j]
                        child2Gen[j] = parent1.chromosomeBinary[variable][j]

                child1Chromosome.append(child1Gen)
                child2Chromosome.append(child2Gen)

            child1 = Individual(None, child1Chromosome)
            child2 = Individual(None, child2Chromosome)

            individualAfterCross.extend([child1, child2])

    newPopulation = Population(population.variableNums)
    newPopulation.individuals = np.array(individualAfterCross)

    return newPopulation


def addRandomIndividualIfOdd(population: Population, lowerLimit: float, upperLimit: float):
    if len(population.individuals) % 2 != 0:
        randomChromosome = np.random.uniform(lowerLimit, upperLimit, population.variableNums)
        randomIndividual = Individual(randomChromosome, None)
        population.individuals = np.append(population.individuals, randomIndividual)


def arithmeticCrossover(population: Population, probability: float, lowerLimit: float, upperLimit: float) -> Population:
    individualAfterCross = []
    k = 0.25

    for i in range(0, len(population.individuals), 2):
        parent1 = population.individuals[i]
        parent2 = population.individuals[i + 1]
        child1Chromosome = []
        child2Chromosome = []

        if random.random() > probability:
            for variable in range(population.variableNums):
                child1Chromosome.append(population.individuals[i].getChromosome()[variable])
                child2Chromosome.append(population.individuals[i + 1].getChromosome()[variable])
        else:
            for variable in range(population.variableNums):
                child1Gen = validateGen(k * parent1.chromosome[variable] + (1 - k) * parent2.chromosome[variable],
                                        lowerLimit, upperLimit)
                child2Gen = validateGen(k * parent2.chromosome[variable] + (1 - k) * parent1.chromosome[variable],
                                        lowerLimit, upperLimit)
                child1Chromosome.append(child1Gen)
                child2Chromosome.append(child2Gen)

        child1 = Individual(child1Chromosome)
        child2 = Individual(child2Chromosome)

        individualAfterCross.extend([child1, child2])

    newPopulation = Population(population.variableNums)
    newPopulation.individuals = np.array(individualAfterCross)

    return newPopulation


def blendACrossover(population: Population, probability: float, lowerLimit: float, upperLimit: float) -> Population:
    individualAfterCross = []
    a = 0.25

    for i in range(0, len(population.individuals), 2):
        parent1 = population.individuals[i]
        parent2 = population.individuals[i + 1]
        child1Chromosome = []
        child2Chromosome = []

        if random.random() > probability:
            for variable in range(population.variableNums):
                child1Chromosome.append(population.individuals[i].getChromosome()[variable])
                child2Chromosome.append(population.individuals[i + 1].getChromosome()[variable])
        else:
            for variable in range(population.variableNums):
                ad = abs(parent1.chromosome[variable] - parent2.chromosome[variable]) * a
                minBlend = min(parent1.chromosome[variable], parent2.chromosome[variable]) - ad
                maxBlend = max(parent1.chromosome[variable], parent2.chromosome[variable]) + ad
                child1Gen = random.uniform(minBlend, maxBlend)
                child2Gen = random.uniform(minBlend, maxBlend)
                child1Chromosome.append(validateGen(child1Gen, lowerLimit, upperLimit))
                child2Chromosome.append(validateGen(child2Gen, lowerLimit, upperLimit))

        child1 = Individual(child1Chromosome)
        child2 = Individual(child2Chromosome)

        individualAfterCross.extend([child1, child2])

    newPopulation = Population(population.variableNums)
    newPopulation.individuals = np.array(individualAfterCross)

    return newPopulation


def blendABCrossover(population: Population, probability: float, lowerLimit: float, upperLimit: float) -> Population:
    individualAfterCross = []
    a = 0.25
    b = 0.30

    for i in range(0, len(population.individuals), 2):
        parent1 = population.individuals[i]
        parent2 = population.individuals[i + 1]
        child1Chromosome = []
        child2Chromosome = []

        if random.random() > probability:
            for variable in range(population.variableNums):
                child1Chromosome.append(population.individuals[i].getChromosome()[variable])
                child2Chromosome.append(population.individuals[i + 1].getChromosome()[variable])
        else:
            for variable in range(population.variableNums):
                ad = abs(parent1.chromosome[variable] - parent2.chromosome[variable]) * a
                bd = abs(parent1.chromosome[variable] - parent2.chromosome[variable]) * b
                minBlend = min(parent1.chromosome[variable], parent2.chromosome[variable]) - ad
                maxBlend = max(parent1.chromosome[variable], parent2.chromosome[variable]) + bd
                child1Gen = random.uniform(minBlend, maxBlend)
                child2Gen = random.uniform(minBlend, maxBlend)
                child1Chromosome.append(validateGen(child1Gen, lowerLimit, upperLimit))
                child2Chromosome.append(validateGen(child2Gen, lowerLimit, upperLimit))

        child1 = Individual(child1Chromosome)
        child2 = Individual(child2Chromosome)

        individualAfterCross.extend([child1, child2])

    newPopulation = Population(population.variableNums)
    newPopulation.individuals = np.array(individualAfterCross)

    return newPopulation


def averageCrossover(population: Population, probability: float) -> Population:
    individualAfterCross = []

    for i in range(0, len(population.individuals), 2):
        parent1 = population.individuals[i]
        parent2 = population.individuals[i + 1]
        child1Chromosome = []

        if random.random() > probability:
            for variable in range(population.variableNums):
                child1Chromosome.append(population.individuals[i].getChromosome()[variable])
        else:
            for variable in range(population.variableNums):
                child1Gen = np.mean([parent1.chromosome[variable], parent2.chromosome[variable]])
                child1Chromosome.append(child1Gen)

        child1 = Individual(child1Chromosome)

        individualAfterCross.extend([child1])

    newPopulation = Population(population.variableNums)
    newPopulation.individuals = np.array(individualAfterCross)

    return newPopulation


def flatCrossover(population: Population, probability: float) -> Population:
    individualAfterCross = []

    for i in range(0, len(population.individuals), 2):
        parent1 = population.individuals[i]
        parent2 = population.individuals[i + 1]
        child1Chromosome = []

        if random.random() > probability:
            for variable in range(population.variableNums):
                child1Chromosome.append(population.individuals[i].getChromosome()[variable])
        else:
            for variable in range(population.variableNums):
                child1Gen = random.uniform(parent1.chromosome[variable], parent2.chromosome[variable])
                child1Chromosome.append(child1Gen)

        child1 = Individual(child1Chromosome)

        individualAfterCross.extend([child1])

    newPopulation = Population(population.variableNums)
    newPopulation.individuals = np.array(individualAfterCross)

    return newPopulation


def heuristicCrossover(population: Population, probability: float, maximization: bool, lowerLimit: float,
                       upperLimit: float) -> Population:
    individualAfterCross = []

    for i in range(0, len(population.individuals), 2):
        k = random.uniform(0, 1)
        parent1 = population.individuals[i]
        parent2 = population.individuals[i + 1]
        child1Chromosome = []

        if parent1.y > parent2.y and maximization is False:
            temp = parent1
            parent1 = parent2
            parent2 = temp

        elif parent1.y < parent2.y and maximization is True:
            temp = parent1
            parent1 = parent2
            parent2 = temp

        if parent2.y > parent1.y and maximization is False:
            if random.random() > probability:
                for variable in range(population.variableNums):
                    child1Chromosome.append(population.individuals[i].getChromosome()[variable])
            else:
                for variable in range(population.variableNums):
                    child1Gen = k * (parent2.chromosome[variable] - parent1.chromosome[variable]) + parent1.chromosome[
                        variable]
                    child1Chromosome.append(child1Gen)
        if parent2.y < parent1.y and maximization is True:
            if random.random() > probability:
                for variable in range(population.variableNums):
                    child1Chromosome.append(population.individuals[i].getChromosome()[variable])
            else:
                for variable in range(population.variableNums):
                    child1Gen = k * (parent2.chromosome[variable] - parent1.chromosome[variable]) + parent1.chromosome[
                        variable]
                    child1Chromosome.append(child1Gen)
        else:
            for variable in range(population.variableNums):
                child1Chromosome.append(population.individuals[i].getChromosome()[variable])

        child1 = Individual(child1Chromosome)

        individualAfterCross.extend([child1])

    newPopulation = Population(population.variableNums)
    newPopulation.individuals = np.array(individualAfterCross)

    return newPopulation
