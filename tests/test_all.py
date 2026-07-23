import pytest

import ecabc.utils as abc_utils
from ecabc import ABC, Bee, Parameter


def _objective_function(params):
    return sum(params)


def _objective_function_kwargs(params, my_kwarg):
    return sum(params) + my_kwarg


# utils.py


def test_apply_mutation():
    params = [Parameter(0, 10, True) for _ in range(3)]
    curr_params = [5, 5, 5]
    mut_params = abc_utils.apply_mutation(curr_params, params)
    assert curr_params != mut_params


def test_call_obj_fn():
    param_vals = [2, 2, 2]
    ret_params, result = abc_utils.call_obj_fn(param_vals, _objective_function, {})
    assert result == 6
    assert ret_params == param_vals
    fn_args = {"my_kwarg": 2}
    ret_params, result = abc_utils.call_obj_fn(
        param_vals, _objective_function_kwargs, fn_args
    )
    assert result == 8
    assert param_vals == ret_params


def test_choose_bee():
    bee_1 = Bee([0], 100000000000000000000, 0)
    bee_2 = Bee([0], 0, 0)
    chosen_bee = abc_utils.choose_bee([bee_1, bee_2])
    assert chosen_bee == bee_2


def test_determine_best_bee():
    bee_1 = Bee([10], 10, 0)
    bee_2 = Bee([0], 0, 0)
    bee_2_fitness = bee_2._fitness_score
    bee_2_ret_val = bee_2._obj_fn_val
    bee_2_params = bee_2._params
    _fit, _ret, _param = abc_utils.determine_best_bee([bee_1, bee_2])
    assert _fit == bee_2_fitness
    assert _ret == bee_2_ret_val
    assert _param == bee_2_params


# parameter.py


def test_param_init():
    param = Parameter(0, 10, False)
    assert param._restrict is False
    param = Parameter(0, 10)
    assert param._restrict is True
    assert param._dtype is int
    assert param._min_val == 0
    assert param._max_val == 10


def test_rand_val():
    for _ in range(100):
        param = Parameter(0, 10)
        rand_val = param.rand_val
        assert rand_val >= 0
        assert rand_val <= 10
        assert isinstance(rand_val, int)
    param = Parameter(0.0, 10.0)
    rand_val = param.rand_val
    assert isinstance(rand_val, float)


def test_mutate():
    param = Parameter(0, 10)
    rand_val = param.rand_val
    for _ in range(1000):
        mutation = param.mutate(rand_val)
        if mutation < 0 or mutation > 10:
            raise ValueError("Mutation outside min/max bounds")
    param = Parameter(0, 3, False)
    rand_val = param.rand_val
    outside_bounds = False
    mutation = param.mutate(rand_val)
    while True:
        if mutation < 0 or mutation > 3:
            outside_bounds = True
            break
        mutation = param.mutate(mutation)
    assert outside_bounds is True


# abc.py


def test_colony_init():
    c = ABC(10, _objective_function)
    assert c._num_employers == 10
    assert c._obj_fn == _objective_function
    kwargs = {"my_kwarg": 2}
    c = ABC(10, _objective_function_kwargs, kwargs)
    assert c._obj_fn_args == kwargs
    c = ABC(10, _objective_function, num_processes=8)
    assert c._num_processes == 8
    with pytest.raises(ReferenceError):
        c = ABC(10, None)


def test_no_bees():
    c = ABC(10, _objective_function)
    assert c.best_fitness == 0
    assert c.best_ret_val is None
    assert c.best_params == {}
    assert c.average_fitness is None
    assert c.average_ret_val is None
    with pytest.raises(RuntimeError):
        c.search()


def test_add_parameter():
    c = ABC(10, _objective_function)
    c.add_param(0, 1)
    c.add_param(2, 3)
    c.add_param(4, 5)
    assert len(c._params) == 3
    assert c._params[0]._min_val == 0
    assert c._params[0]._max_val == 1
    assert c._params[1]._min_val == 2
    assert c._params[1]._max_val == 3
    assert c._params[2]._min_val == 4
    assert c._params[2]._max_val == 5
    assert c._params[0]._dtype is int
    c.add_param(0.0, 1.0)
    assert c._params[3]._dtype is float
    assert c._params[0]._restrict is True
    c.add_param(0, 1, False)
    assert c._params[4]._restrict is False


def test_initialize():
    c = ABC(10, _objective_function)
    c.add_param(0, 10)
    c.add_param(0, 10)
    c.initialize()
    assert len(c._bees) == 20


def test_search_and_stats():
    c = ABC(10, _objective_function)
    c.add_param(0, 0)
    c.add_param(0, 0)
    c.initialize()
    for _ in range(50):
        c.search()
    assert c.best_fitness == 1
    assert c.best_ret_val == 0
    assert c.best_params == {"P0": 0, "P1": 0}


def test_kwargs():
    c = ABC(10, _objective_function_kwargs, {"my_kwarg": 2})
    c.add_param(0, 0)
    c.add_param(0, 0)
    c.initialize()
    for _ in range(50):
        c.search()
    assert c.best_ret_val == 2


def test_multiprocessing():
    c = ABC(20, _objective_function, num_processes=4)
    assert c._num_processes == 4
    c.add_param(0, 10)
    c.add_param(0, 10)
    c.initialize()
    c.search()


def test_custom_param_name():
    c = ABC(20, _objective_function)
    c.add_param(0, 10, name="int1")
    c.add_param(0, 10, name="int2")
    c.initialize()
    for _ in range(50):
        c.search()
    assert c.best_params == {"int1": 0, "int2": 0}


# bee.py


def test_bee_init():
    bee = Bee([0, 0, 0], 0, 1, True)
    assert bee._is_employer is True
    bee = Bee([0, 0, 0], 0, 1)
    assert bee._is_employer is False
    assert bee._params == [0, 0, 0]
    assert bee._obj_fn_val == 0
    assert bee._fitness_score == 1
    assert bee._stay_limit == 1


def test_abandon():
    bee = Bee([0, 0, 0], 0, 2)
    result = bee.abandon
    assert result is False
    result = bee.abandon
    assert result is True


def test_calc_fitness():
    result = Bee.calc_fitness(0)
    assert result == 1
    result = Bee.calc_fitness(-1)
    assert result == 2


def test_is_better_food():
    bee = Bee([0, 0, 1], 1, 1)
    result = bee.is_better_food(0)
    assert result is True
    result = bee.is_better_food(2)
    assert result is False
