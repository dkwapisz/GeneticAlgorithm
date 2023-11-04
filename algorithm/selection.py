import numpy as np

from algorithm.Individual import Individual
from algorithm.Population import Population


def selectionOfTheBest(population: np.array(Individual), numParents: int, maximization=False) -> (np.array, np.array):
    sortedPopulation = sorted(population.getIndividuals(), key=lambda x: x.getY(), reverse=maximization)
    selectedIndividuals = sortedPopulation[:numParents]

    selectedPopulation = Population(population.getVariableNums())
    selectedPopulation.setIndividuals(selectedIndividuals)
    population.setRestOfIndividualsAfterSelection(selectedIndividuals)

    return selectedPopulation


def tournamentSelection(population: np.array(Individual), tournamentSize: int, numSelected=1, maximization=False) -> (
        np.array, np.array):
    selectedIndividuals = []
    for _ in range(tournamentSize):
        tournamentPool = np.random.choice(population.getIndividuals(), size=tournamentSize, replace=False)
        tournamentWinner = max(tournamentPool, key=lambda x: x.getY()) if maximization else min(tournamentPool,
                                                                                                key=lambda x: x.getY())
        selectedIndividuals.append(tournamentWinner)

    selectedPopulation = Population(population.getVariableNums())
    selectedPopulation.setIndividuals(selectedIndividuals)
    population.setRestOfIndividualsAfterSelection(selectedIndividuals)

    return selectedPopulation


def rouletteWheelSelection(population: np.array(Individual), numSelected: int) -> (np.array, np.array):
    fitnessValue = [ind.getY() for ind in population.getIndividuals()]
    totalFitness = sum(fitnessValue)
    probabilities = [fit / totalFitness for fit in fitnessValue]

    selectedIndividuals = []
    for _ in range(numSelected):
        chosenIndex = np.random.choice(range(len(population.getIndividuals())), p=probabilities)
        selectedIndividuals.append(population.getIndividuals()[chosenIndex])

    selectedPopulation = Population(population.getVariableNums())
    selectedPopulation.setIndividuals(selectedIndividuals)
    population.setRestOfIndividualsAfterSelection(selectedIndividuals)

    return selectedPopulation
