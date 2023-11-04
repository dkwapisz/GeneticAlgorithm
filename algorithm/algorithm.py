from algorithm.Population import Population
from algorithm.crossover import arithmeticCrossover, averageCrossover, blendABCrossover, blendACrossover, flatCrossover, heuristicCrossover, onePointCrossover, threePointCrossover, twoPointCrossover, uniformCrossover, \
    addRandomIndividualIfOdd
from algorithm.mutation import boundaryMutation, gaussMutation, indexMutation, inversion, onePointMutation, uniformMutation
from algorithm.selection import rouletteWheelSelection, selectionOfTheBest, tournamentSelection


def algorithmStart(variablesNum: int, iterations: int, lowerLimit: float, upperLimit: float, populationAmount: int,
                   precision: int, epochsAmount: int, eliteStrategyAmount: int, crossProbability: float,
                   mutationProbability: float, inversionProbability: float, bestAndTournamentChromosomeAmount: int,
                   selectionType: str, crossMethod: str, mutationMethod: str, maximization: bool,
                   decimalAlgorithm: bool, ui):
    print(f"Interval Start: {lowerLimit}\n"
          f"Interval End: {upperLimit}\n"
          f"Variables num: {variablesNum}\n"
          f"Iterations: {iterations}\n"
          f"Population Amount: {populationAmount}\n"
          f"Precision: {precision}\n"
          f"Epochs Amount: {epochsAmount}\n"
          f"Elite Strategy Amount: {eliteStrategyAmount}\n"
          f"Cross Probability: {crossProbability}\n"
          f"Mutation Probability: {mutationProbability}\n"
          f"Inversion Probability: {inversionProbability}\n"
          f"Best and Tournament Chromosome Amount: {bestAndTournamentChromosomeAmount}\n"
          f"Selection Type: {selectionType}\n"
          f"Cross Method: {crossMethod}\n"
          f"Mutation Method: {mutationMethod}\n"
          f"Maximization: {maximization}")

    bestFromAllIterations = {}

    crossProbability = float(crossProbability)
    mutationProbability = float(mutationProbability)
    inversionProbability = float(inversionProbability)
    lowerLimit = float(lowerLimit)
    upperLimit = float(upperLimit)

    for iteration in range(iterations):
        print(f'--- Iteration: {iteration + 1}/{iterations} ---')

        population = Population(variablesNum)
        population.generateRandomPopulation(lowerLimit, upperLimit, populationAmount)
        population.selectElites(eliteStrategyAmount, maximization)

        for epoch in range(epochsAmount):
            print(f'Epochs: {epoch + 1}/{epochsAmount}')

            # Evaluation
            population.selectElites(eliteStrategyAmount, maximization)

            # Selection
            match selectionType:
                case 'BEST':
                    selectedPopulation = selectionOfTheBest(population, bestAndTournamentChromosomeAmount, maximization)
                case 'TOURNAMENT':
                    selectedPopulation = tournamentSelection(population, bestAndTournamentChromosomeAmount, maximization)
                case 'ROULETTE':
                    selectedPopulation = rouletteWheelSelection(population, bestAndTournamentChromosomeAmount)

            # Binary conversion step
            addRandomIndividualIfOdd(selectedPopulation, lowerLimit, upperLimit)

            if not decimalAlgorithm:
                selectedPopulation.convertPopulationToBinary(lowerLimit, upperLimit, precision)
                # Crossover
                match crossMethod:
                    case 'ONE_POINT [B]':
                        selectedPopulation = onePointCrossover(selectedPopulation, crossProbability)
                    case 'TWO_POINTS [B]':
                        selectedPopulation = twoPointCrossover(selectedPopulation, crossProbability)
                    case 'THREE_POINTS [B]':
                        selectedPopulation = threePointCrossover(selectedPopulation, crossProbability)
                    case 'UNIFORM [B]':
                        selectedPopulation = uniformCrossover(selectedPopulation, crossProbability)
                    case _:
                        selectedPopulation = onePointCrossover(selectedPopulation, crossProbability)

                # Mutation
                match mutationMethod:
                    case 'ONE_POINT [B]':
                        selectedPopulation = onePointMutation(selectedPopulation, mutationProbability)
                    case 'TWO_POINT [B]':
                        selectedPopulation = twoPointCrossover(selectedPopulation, mutationProbability)
                    case 'BOUNDARY [B]':
                        selectedPopulation = boundaryMutation(selectedPopulation, mutationProbability)
                    case _:
                        selectedPopulation = onePointMutation(selectedPopulation, mutationProbability)

                # Inversion
                selectedPopulation = inversion(selectedPopulation, inversionProbability)

                # Decimal conversion step
                selectedPopulation.convertPopulationToDecimal(lowerLimit, upperLimit, precision)

            else:
                # Crossover
                match crossMethod:
                    case 'ARITHMETIC [D]':
                        selectedPopulation = arithmeticCrossover(selectedPopulation, crossProbability, lowerLimit, upperLimit)
                    case 'BLEND_A [D]':
                        selectedPopulation = blendACrossover(selectedPopulation, crossProbability, lowerLimit, upperLimit)
                    case 'BLEND_AB [D]':
                        selectedPopulation = blendABCrossover(selectedPopulation, crossProbability, lowerLimit, upperLimit)
                    case 'AVERAGE [D]':
                        selectedPopulation = averageCrossover(selectedPopulation, crossProbability)
                    case 'FLAT [D]':
                        selectedPopulation = flatCrossover(selectedPopulation, crossProbability)
                    case 'HEURISTIC [D]':
                        selectedPopulation = heuristicCrossover(selectedPopulation, crossProbability, maximization,  lowerLimit, upperLimit)
                    case _:
                        selectedPopulation = arithmeticCrossover(selectedPopulation, crossProbability, lowerLimit, upperLimit)
                # Mutation
                match mutationMethod:
                    case 'UNIFORM [D]':
                        selectedPopulation = uniformMutation(selectedPopulation, mutationProbability, lowerLimit, upperLimit)
                    case 'INDEX [D]':
                        selectedPopulation = indexMutation(selectedPopulation, mutationProbability)
                    case 'GAUSS [D]':
                        selectedPopulation = gaussMutation(selectedPopulation, mutationProbability, lowerLimit, upperLimit)
                    case _:
                        selectedPopulation = uniformMutation(selectedPopulation, mutationProbability, lowerLimit, upperLimit)

            # Final steps
            population.combinePopulations(population.getIndividuals(), selectedPopulation.getIndividuals())
            population.updateAllIndividualsY()
            population.selectElites(eliteStrategyAmount, maximization)

            ui.add_or_update_graph('Closest_Y_value', (epoch, population.getElites()[0].getY()), ('Epoch', 'Y value'))
            ui.add_or_update_graph('Average_Y_value', (epoch, calculate_avg(population.getPopulationResult())),
                                   ('Epoch', 'avg'))
            ui.add_or_update_graph('Standard_Deviation', (epoch, calculate_deviation(population.getPopulationResult())),
                                   ('Epoch', 'deviation'))

            bestFromAllIterations[tuple(population.getElites()[0].getChromosome())] = population.getElites()[0].getY()

        print(f"Best approximation X: {population.getElites()[0].getChromosome()}, y = {population.getElites()[0].getY()} \n")

    bestFromAllIterations = dict(sorted(bestFromAllIterations.items(), key=lambda item: item[1], reverse=maximization))
    print(f"Best after {iterations} iterations of algorithm: X: {list(bestFromAllIterations.keys())[0]}, y: {list(bestFromAllIterations.values())[0]}")

    return list(bestFromAllIterations.keys())[0], list(bestFromAllIterations.values())[0]


def calculate_avg(values):
    size = len(values)
    sum = 0.
    for i in range(size):
        sum += values[i]
    return sum / size


def calculate_deviation(values):
    avg = calculate_avg(values)
    sum = 0.
    size = len(values)
    for i in range(size):
        sum += pow(values[i] - avg, 2)
    return pow(sum / size, 1 / 2)
