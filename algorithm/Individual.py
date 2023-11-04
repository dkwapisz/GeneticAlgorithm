import numpy as np

from algorithm.binaryUtils import decimalToBinaryArray, binaryArrayToDecimal
from algorithm.functionUtils import ackleyFunction


# Single Individual(x array : y result)
class Individual:

    def __init__(self, chromosome: np.array([]), chromosomeBinary=None):
        self.chromosome = chromosome
        self.chromosomeBinary = chromosomeBinary
        self.y = 0
        self.updateY()

    def getChromosome(self):
        return self.chromosome

    def getY(self):
        return self.y

    def setChromosome(self, chromosome: np.array([])):
        self.chromosome = chromosome

    def setY(self, y: float):
        self.y = y

    def getChromosomeBinary(self):
        return self.chromosomeBinary

    def getChromosomeBinaryLength(self):
        return self.chromosomeBinary[0].size

    def updateY(self):
        if self.chromosome is not None:
            self.y = ackleyFunction(self.chromosome)
        else:
            self.y = 0

    def convertChromosomeToBinary(self, lowerLimit: float, upperLimit: float, precision: int):
        self.chromosomeBinary = []
        for x in self.chromosome:
            binaryArray = decimalToBinaryArray(x, lowerLimit, upperLimit, precision)
            self.chromosomeBinary.append(binaryArray)

    def convertBinaryChromosomeToDecimal(self, lowerLimit: float, upperLimit: float, precision: int):
        self.chromosome = np.array([])
        for xBinary in self.chromosomeBinary:
            self.chromosome = np.append(self.chromosome,
                                        binaryArrayToDecimal(xBinary, lowerLimit, upperLimit, precision))

    def __eq__(self, other):
        if not isinstance(other, Individual):
            return False
        return np.array_equal(self.chromosome, other.chromosome)

    def __hash__(self):
        return hash(tuple(self.chromosome))


def validateGen(chromosomeGen: float, lowerLimit: float, upperLimit: float) -> float:
    if chromosomeGen < lowerLimit:
        chromosomeGen = lowerLimit
    elif chromosomeGen > upperLimit:
        chromosomeGen = upperLimit
    return chromosomeGen
