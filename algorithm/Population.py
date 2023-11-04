import numpy as np

from algorithm.Individual import Individual


# Single Population: population array of individuals
class Population:

    def __init__(self, variableNums):
        self.variableNums = variableNums
        self.individuals = None
        self.eliteIndividuals = None

    def generateRandomPopulation(self, intervalStart: float, intervalEnd: float, populationAmount: int):
        self.individuals = []
        for _ in range(populationAmount):
            chromosome = np.random.uniform(intervalStart, intervalEnd, self.variableNums)
            self.individuals.append(Individual(chromosome))

        self.individuals = np.array(self.individuals)

    def getVariableNums(self):
        return self.variableNums

    def setVariableNums(self, variableNums):
        self.variableNums = variableNums

    def getIndividuals(self):
        return self.individuals

    def setIndividuals(self, individuals):
        self.individuals = individuals

    def getElites(self):
        return self.eliteIndividuals

    def getPopulationResult(self):
        result = []
        for individual in self.individuals:
            result.append(individual.getY())
        return result

    def combinePopulations(self, individuals1, individuals2):
        self.individuals = np.hstack((individuals1, individuals2))

    def updateAllIndividualsY(self):
        for individual in self.individuals:
            individual.updateY()
        for eliteIndividual in self.eliteIndividuals:
            eliteIndividual.updateY()

    def selectElites(self, numElites: int, maximization: bool):
        if self.eliteIndividuals is not None:
            self.individuals = np.hstack((self.eliteIndividuals, self.individuals))

        numElites = int(numElites)
        if numElites == 0:
            numElites = 1

        sortedPopulation = sorted(self.individuals, key=lambda x: x.getY(), reverse=maximization)
        elites = sortedPopulation[:numElites]
        self.eliteIndividuals = np.array(elites)

    def setRestOfIndividualsAfterSelection(self, selectedIndividuals):
        keepMask = np.isin(self.individuals, selectedIndividuals, invert=True)
        self.individuals = self.individuals[keepMask]

    def convertPopulationToBinary(self, lowerLimit: float, upperLimit: float, precision: int):
        for individual in self.individuals:
            individual.convertChromosomeToBinary(lowerLimit, upperLimit, precision)

    def convertPopulationToDecimal(self, lowerLimit: float, upperLimit: float, precision: int):
        for individual in self.individuals:
            individual.convertBinaryChromosomeToDecimal(lowerLimit, upperLimit, precision)

    def __eq__(self, other):
        if not isinstance(other, Population):
            return False
        return np.array_equal(self.individuals, other.individuals)

    def __hash__(self):
        return hash(tuple(self.individuals))
    
