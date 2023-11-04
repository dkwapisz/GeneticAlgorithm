from libs.patterns.singleton import Singleton


class SimpleSetting:
    _method = None
    _probability = 0

    def __init__(self) -> None:
        pass

    def set_method(self, value):
        self._method = value

    def get_method(self):
        return self._method

    def set_probability(self, value):
        self._probability = value

    def get_probability(self):
        return self._probability


class Settings(metaclass=Singleton):
    _variable_amount = 1
    _epochs = 0
    _range = {"start": 0, "end": 0}
    _population = 0
    _precision = None
    _selection_type = "TOURNAMENT"
    _selection_best_percentage = 0.1
    _best_chromosomes_tournament_group_size = 50
    _elite_strategy = {"should_use_elite_strategy": True, "integer": 1, "type": "percentage"}
    cross_settings = SimpleSetting()
    mutation_settings = SimpleSetting()
    inversion_settings = SimpleSetting()
    _is_maximum_optimization = False

    def __init__(self) -> None:
        pass

    # def _validate_numeric_input(self, value, allow_negative):
    #    return value.isnumeric() and (allow_negative or int(value) > 0)
    def set_epochs(self, value):
        self._epochs = int(value)

    def get_epochs(self):
        return self._epochs

    def set_variable_amount(self, value):
        self._variable_amount = int(value)

    def get_variable_amount(self):
        return self._variable_amount

    def set_range(self, start, end):
        self._range = {"start": float(start), "end": float(end)}

    def get_range(self):
        return self._range

    def set_population(self, value):
        self._population = int(value)

    def get_population(self):
        return self._population

    def set_precision(self, value):
        print(value)
        self._precision = int(value)

    def get_precision(self):
        return self._precision

    def set_selection_type(self, value):
        self._selection_type = value

    def get_selection_type(self):
        return self._selection_type

    def set_selection_best_percentage(self, value):
        self._selection_best_percentage = float(value)

    def set_best_chromosomes_tournament_group_size(self, value):
        self._best_chromosomes_tournament_group_size = int(value)

    def get_chromosomes(self):
        return self._best_chromosomes_tournament_group_size

    def get_selection_settings(self):
        match self._selection_type:
            case "TOURNAMENT":
                return self.set_best_chromosomes_tournament_group_size
            case "BEST":
                return self._selection_best_percentage
            case _:
                return None

    def set_should_use_elite_strategy_(self, value):
        self._elite_strategy["should_use_elite_strategy"] = bool(value)

    def should_use_elite_strategy(self):
        return self._elite_strategy["should_use_elite_strategy"]

    def set_elite_settings(self, integer):
        self._elite_strategy["integer"] = int(integer)

    def get_elite_strategy_integer(self):
        match self._elite_strategy["type"]:
            case "percentage":
                return self._population * (self._elite_strategy["integer"] / 100)
            case _:
                return self._elite_strategy["integer"]

    def get_elite_strategy_type(self):
        if self.is_strategy_elite():
            return self._elite_strategy["type"]
        return "integer"

    def is_strategy_elite(self):
        return self._elite_strategy["should_use_elite_strategy"]

    def set_is_maximum(self, value):
        self._is_maximum_optimization = str(value) == "True"

    def get_is_maximum(self):
        return self._is_maximum_optimization
