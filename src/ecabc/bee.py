#!/usr/bin/env python
#
#  ecabc/bee.py
#  v.3.0.0
#
#  Developed in 2019 by Sanskriti Sharma <sanskriti_sharma@student.uml.edu>,
#  Hernan Gelaf-Romer <hernan_gelafromer@student.uml.edu>, and Travis Kessler
#  <Travis_Kessler@student.uml.edu>
#
#  bee.py: contains Bee object, which houses information relevant to a
#  specific solution being investigated by an individual bee
#

# Stdlib. imports


class Bee:
    def __init__(
        self,
        params: list,
        obj_fn_val: int | float,
        stay_limit: int,
        is_employer: bool = False,
    ):
        """Bee object: houses bee-specific information such as its current
        set of parameters, the objective function value resulting from its,
        current parameters, maximum number of cycles it can stay at its
        current food source, and whether it is an employer bee or not

        Args:
            params (list): list of current set of parameters, int or float
            obj_fn_val (int, float): value returned by objective function when
                supplied parameters are supplied
            stay_limit (int): maximum number of cycles the bee can stay at its
                current food source
            is_employer (bool): `True` if employer, `False` if onlooker
        """

        self._params = params
        self._obj_fn_val = obj_fn_val
        self._fitness_score = self.calc_fitness(obj_fn_val)
        self._stay_limit = stay_limit
        self._stay_count = 0
        self._is_employer = is_employer

    @property
    def abandon(self) -> bool:
        """When called, increment how many times the bee has stayed at its
        current food source; if reached stay limit, return `True` else `False`
        """

        self._stay_count += 1
        if self._stay_count >= self._stay_limit:
            return True
        else:
            return False

    @staticmethod
    def calc_fitness(obj_fn_val: int | float) -> float:
        """Static method: Bee.calc_fitness: Calculates fitness score based on
        objective function value, using the equation:

        fitness = 1 / (1 + ofv)     if ofv >= 0
        fitness = 1 + abs(ofv)      if ofv < 0

        Where ofv is the objective function value and fitness is the resulting
        fitness score

        Args:
            obj_fn_val (int, float): value obtained from objective function

        Returns:
            float: resulting fitness score
        """

        if obj_fn_val >= 0:
            return 1 / (obj_fn_val + 1)
        else:
            return 1 + abs(obj_fn_val)

    def is_better_food(self, obj_fn_val: int | float) -> bool:
        """Bee.is_better_food: determines if objective function value
        resulting from a new food source is better than the bee's current food
        source

        Args:
            obj_fn_val (int, float): value resulting from objective function
                with new food

        Returns:
            bool: `True` if better food source else `False`
        """

        if self.calc_fitness(obj_fn_val) > self._fitness_score:
            return True
        else:
            return False
