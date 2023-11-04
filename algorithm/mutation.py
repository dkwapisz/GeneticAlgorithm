import random

import numpy as np
from algorithm.Individual import validateGen

from algorithm.Population import Population


def boundaryMutation(population: Population, probability: float) -> np.array:
    for i in range(0, len(population.individuals), 2):
        for variable in range(population.variableNums):
            if random.random() > probability:
                continue

            population.getIndividuals()[i].getChromosomeBinary()[variable][-1] = 1 if \
                population.getIndividuals()[i].getChromosomeBinary()[variable][-1] == 0 else 0

    return population


def onePointMutation(population: Population, probability: float) -> np.array:
    for i in range(0, len(population.individuals), 2):
        for variable in range(population.variableNums):
            if random.random() > probability:
                continue

            point = random.sample(range(population.getIndividuals()[i].getChromosomeBinaryLength() - 1), 1)
            population.getIndividuals()[i].getChromosomeBinary()[variable][point] = 1 if \
                population.getIndividuals()[i].getChromosomeBinary()[variable][point] == 0 else 0

    return population


def twoPointMutation(population: Population, probability: float) -> np.array:
    for i in range(0, len(population.individuals), 2):
        for variable in range(population.variableNums):
            if random.random() > probability:
                continue

            point = random.sample(range(population.getIndividuals()[i].getChromosomeBinaryLength() - 1), 2)
            population.getIndividuals()[i].getChromosomeBinary()[variable][point[0]] = 1 if \
                population.getIndividuals()[i].getChromosomeBinary()[variable][point[0]] == 0 else 0
            population.getIndividuals()[i].getChromosomeBinary()[variable][point[1]] = 1 if \
                population.getIndividuals()[i].getChromosomeBinary()[variable][point[1]] == 0 else 0

    return population


def inversion(population: Population, probability: float) -> np.array:
    for i in range(0, len(population.individuals), 2):
        for variable in range(population.variableNums):
            if random.random() > probability:
                continue

            point1, point2 = random.sample(range(population.getIndividuals()[i].getChromosomeBinaryLength()), 2)

            if point1 > point2:
                point1, point2 = point2, point1

            population.getIndividuals()[i].getChromosomeBinary()[variable][point1:point2 + 1] = \
                population.getIndividuals()[i].getChromosomeBinary()[variable][point1:point2 + 1][::-1]

    return population


def uniformMutation(population: Population, probability: float, lowerLimit: float, upperLimit: float) -> np.array:
    for i in range(0, len(population.individuals), 2):
        if random.random() > probability:
            continue
        randomVariable = random.randint(0, population.variableNums - 1)
        population.getIndividuals()[i].getChromosome()[randomVariable] = random.uniform(lowerLimit, upperLimit)
    return population


def indexMutation(population: Population, probability: float) -> np.array:
    for i in range(0, len(population.individuals), 2):
        if random.random() > probability:
            continue
        if population.variableNums == 1:
            continue
        temp = population.getIndividuals()[i].getChromosome()[0]
        for variable in range(population.variableNums - 1):
            population.getIndividuals()[i].getChromosome()[variable] = population.getIndividuals()[i].getChromosome()[
                variable + 1]
        population.getIndividuals()[i].getChromosome()[population.variableNums - 1] = temp
    return population


def gaussMutation(population: Population, probability: float, lowerLimit: float, upperLimit: float) -> np.array:
    for i in range(0, len(population.individuals), 2):
        if random.random() > probability:
            continue
        for variable in range(population.variableNums - 1):
            population.getIndividuals()[i].getChromosome()[variable] = validateGen(
                population.getIndividuals()[i].getChromosome()[variable] + random.gauss(0, 1), lowerLimit, upperLimit)
    return population
