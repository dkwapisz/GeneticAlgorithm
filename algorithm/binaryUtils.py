import math

import numpy as np


# Precision -> how many digits after comma
def decimalToBinaryArray(number: float, lowerLimit: float, upperLimit: float, precision: int) -> np.array:
    scaledDecimal = (number - lowerLimit) / (upperLimit - lowerLimit)

    binaryArray = []
    for i in range(calculateBitsLength(lowerLimit, upperLimit, precision)):
        scaledDecimal *= 2
        if scaledDecimal >= 1:
            binaryArray.append(1)
            scaledDecimal -= 1
        else:
            binaryArray.append(0)

    return np.array(binaryArray)


def binaryArrayToDecimal(binary_array: np.array, lowerLimit: float, upperLimit: float, precision: int) -> float:
    return round((lowerLimit + decimal(binary_array) * (
            (upperLimit - lowerLimit) / (2 ** calculateBitsLength(lowerLimit, upperLimit, precision) - 1))), precision)


def calculateBitsLength(lowerLimit: float, upperLimit: float, precision: int) -> int:
    return int(math.ceil(math.log2((upperLimit - lowerLimit) * (10 ** precision) + 1)))


def decimal(binary_array):
    decimalValue = 0
    for bit in binary_array:
        decimalValue = decimalValue * 2 + bit
    return decimalValue


def binaryPopulationToDecimalPopulation(binary_array: np.array, lowerLimit: float, upperLimit: float, precision: int,
                                        populationAmount: int) -> np.array:
    population = np.array([])
    for x in range(populationAmount):
        population = np.append(binaryArrayToDecimal(binary_array[x], lowerLimit, upperLimit, precision), population)
    return population


def decimalPopulationToBinaryPopulation(population: np.array, lowerLimit: float, upperLimit: float,
                                        precision: int) -> np.array:
    binaryPopulation = np.array([])
    for x in range(population.size):
        binaryPopulation = np.append(decimalToBinaryArray(population[x], lowerLimit, upperLimit, precision),
                                     binaryPopulation)
    binaryPopulation = binaryPopulation.reshape(population.size, -1)
    return binaryPopulation

# Testing
# if __name__ == "__main__":
#     decimalNumber = 2.6458963789
#     precision = 6
#     lowerLimit = -10
#     upperLimit = 10
#
#     binaryRepresentation = decimalToBinaryArray(decimalNumber, lowerLimit, upperLimit, precision)
#     reversedDecimal = binaryArrayToDecimal(binaryRepresentation, lowerLimit, upperLimit, precision)
#
#     print("Decimal representation: {}, Precision: {}, LowerLimit: {}, UpperLimit: {}".format(decimalNumber, precision,
#                                                                                              lowerLimit, upperLimit))
#     print("\t")
#     print("Binary representation: ", binaryRepresentation)
#     print("Decimal representation [DECODED]: ", reversedDecimal)
#     print("\t")
#
#     # Test ze znaną liczbą binarną - 8.48155
#     binaryRepresentation2 = np.array([1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1])
#     reversedDecimal2 = binaryArrayToDecimal(binaryRepresentation2, lowerLimit, upperLimit, precision)
#     print("Given number: ", 8.48155)
#     print("Example correct binary: ", binaryRepresentation2)
#     print("Decoded correct binary: ", reversedDecimal2)
