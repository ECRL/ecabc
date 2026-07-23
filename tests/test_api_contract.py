"""Lock public API signatures, exceptions, and characterization (design §8 / §11.1)."""

from __future__ import annotations

import inspect
import random

import pytest

import ecabc.abc as abc_mod
import ecabc.utils as abc_utils
from ecabc import ABC, Bee, Parameter, __version__

_EMPTY = inspect.Parameter.empty

# Expected (name, default) in declaration order. Defaults only — not annotations.
# `self` is omitted; locks are for the caller-facing surface.
_EXPECTED_SIGNATURES: dict[str, list[tuple[str, object]]] = {
    "__init__": [
        ("num_employers", _EMPTY),
        ("objective_fn", _EMPTY),
        ("obj_fn_args", {}),
        ("num_processes", 1),
    ],
    "add_param": [
        ("min_val", _EMPTY),
        ("max_val", _EMPTY),
        ("restrict", True),
        ("name", None),
    ],
    "initialize": [],
    "search": [],
}


@pytest.mark.parametrize("name", list(_EXPECTED_SIGNATURES))
def test_abc_signature_names_and_defaults(name: str) -> None:
    method = getattr(ABC, name)
    expected = _EXPECTED_SIGNATURES[name]
    params = [
        p for p in inspect.signature(method).parameters.values() if p.name != "self"
    ]

    actual = [(p.name, p.default) for p in params]
    assert actual == expected, (
        f"ABC.{name} signature drift:\n  expected={expected!r}\n  actual  ={actual!r}"
    )


def _minimize(params: list) -> float:
    return float(sum(params))


def test_non_callable_objective_raises_reference_error() -> None:
    with pytest.raises(ReferenceError):
        ABC(10, None)  # type: ignore[arg-type]


def test_add_param_after_initialize_raises_runtime_error() -> None:
    colony = ABC(2, _minimize)
    colony.add_param(0, 1)
    colony.initialize()
    with pytest.raises(RuntimeError):
        colony.add_param(0, 1)


def test_search_before_initialize_raises_runtime_error() -> None:
    colony = ABC(2, _minimize)
    colony.add_param(0, 1)
    with pytest.raises(RuntimeError):
        colony.search()


def test_second_initialize_emits_runtime_warning() -> None:
    colony = ABC(2, _minimize)
    colony.add_param(0, 1)
    colony.initialize()
    with pytest.warns(RuntimeWarning):
        colony.initialize()


def test_parameter_minmax_type_mismatch_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Parameter(0, 1.0)


def test_default_best_params_keys_are_p_index() -> None:
    random.seed(7)
    colony = ABC(3, _minimize)
    colony.add_param(0, 5)
    colony.add_param(0, 5)
    colony.initialize()
    assert sorted(colony.best_params.keys()) == ["P0", "P1"]


def test_colony_size_is_twice_num_employers_after_initialize() -> None:
    # Colony length is not exposed on the public API; this is the sole
    # private-attribute check for the Phase 0 characterization suite.
    num_employers = 5
    random.seed(11)
    colony = ABC(num_employers, _minimize)
    colony.add_param(0, 10)
    colony.initialize()
    assert len(colony._bees) == 2 * num_employers


def _run_minimize_integers(
    seed: int,
    *,
    num_employers: int = 4,
    num_params: int = 3,
    cycles: int = 15,
) -> tuple[ABC, list]:
    random.seed(seed)
    colony = ABC(num_employers, _minimize)
    for _ in range(num_params):
        colony.add_param(0, 10)
    colony.initialize()
    history = [colony.best_ret_val]
    for _ in range(cycles):
        colony.search()
        history.append(colony.best_ret_val)
    return colony, history


def test_seeded_minimize_integers_characterization() -> None:
    """Seeded minimize-integers oracle (design §8.2 / §8.4)."""
    seed = 123
    colony_a, history = _run_minimize_integers(seed)
    colony_b, _ = _run_minimize_integers(seed)

    assert all(isinstance(v, (int, float)) for v in history)
    assert all(history[i] <= history[i - 1] for i in range(1, len(history)))

    # Golden snapshot for silent algorithm-drift detection.
    assert colony_a.best_ret_val == 0
    assert colony_a.best_params == {"P0": 0, "P1": 0, "P2": 0}
    assert colony_a.best_fitness == 1.0

    assert (
        colony_a.best_ret_val,
        colony_a.best_params,
        colony_a.best_fitness,
    ) == (
        colony_b.best_ret_val,
        colony_b.best_params,
        colony_b.best_fitness,
    )


def test_restrict_false_search_smoke() -> None:
    """Minimal restrict=False path (design Q7); no numeric oracle."""
    random.seed(99)
    colony = ABC(3, _minimize)
    colony.add_param(0, 10, restrict=False)
    colony.add_param(0, 10, restrict=False)
    colony.initialize()
    for _ in range(5):
        colony.search()
    assert isinstance(colony.best_ret_val, (int, float))
    assert isinstance(colony.best_params, dict)


def test_secondary_exports_importable() -> None:
    assert Bee is not None
    assert Parameter is not None
    for name in (
        "apply_mutation",
        "call_obj_fn",
        "choose_bee",
        "determine_best_bee",
    ):
        assert callable(getattr(abc_utils, name))


def test_package_all_matches_frozen_surface() -> None:
    import ecabc

    assert ecabc.__all__ == [
        "ABC",
        "Bee",
        "Parameter",
        "__version__",
        "utils",
    ]
    for name in ecabc.__all__:
        assert hasattr(ecabc, name)


def test_version_is_packaging_metadata_string() -> None:
    assert isinstance(__version__, str)
    assert __version__
    assert __version__ != "2.2.3"


@pytest.mark.parametrize(
    ("obj_fn_val", "expected"),
    [
        (0, 1.0),
        (1, 0.5),
        (-1, 2.0),
    ],
)
def test_bee_calc_fitness_semantics(obj_fn_val: int, expected: float) -> None:
    assert Bee.calc_fitness(obj_fn_val) == expected


def test_parameter_mutate_respects_restrict_true() -> None:
    random.seed(3)
    param = Parameter(0, 10, restrict=True)
    value = param.rand_val
    for _ in range(200):
        value = param.mutate(value)
        assert 0 <= value <= 10


def test_parameter_mutate_can_escape_when_restrict_false() -> None:
    random.seed(5)
    param = Parameter(0, 3, restrict=False)
    value = param.rand_val
    escaped = False
    for _ in range(5000):
        value = param.mutate(value)
        if value < 0 or value > 3:
            escaped = True
            break
    assert escaped


def _squared_sum(params: list) -> float:
    return float(params[0] ** 2 + params[1] ** 2)


def _colony_with_roles(
    employers: list[Bee],
    onlookers: list[Bee],
) -> ABC:
    """Assemble a colony with fixed bee roles (stay limits disable abandon)."""
    colony = ABC(len(employers), _squared_sum)
    colony.add_param(0.0, 1.0)
    colony.add_param(0.0, 1.0)
    bees = employers + onlookers
    for bee in bees:
        bee._stay_limit = 10**9
        bee._stay_count = 0
    colony._bees = bees
    colony._num_employers = len(employers)
    return colony


def test_obj_fn_args_default_not_shared_across_instances() -> None:
    colony_a = ABC(2, _minimize)
    colony_b = ABC(2, _minimize)
    colony_a._obj_fn_args["leak"] = True
    assert "leak" not in colony_b._obj_fn_args
    assert colony_a._obj_fn_args is not colony_b._obj_fn_args


def test_employer_keeps_role_when_accepting_better_food(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Employed bees remain employed after moving to better food (Karaboğa ABC)."""
    stay = 4
    colony = _colony_with_roles(
        employers=[
            Bee([1.0, 1.0], 2.0, stay, True),
            Bee([1.0, 1.0], 2.0, stay, True),
        ],
        onlookers=[
            Bee([0.5, 0.5], 0.5, stay, False),
            Bee([0.5, 0.5], 0.5, stay, False),
        ],
    )
    monkeypatch.setattr(abc_mod, "apply_mutation", lambda curr, params: [0.0, 0.0])

    colony.search()

    n_employers = sum(1 for bee in colony._bees if bee._is_employer)
    assert n_employers == 2
    assert all(bee._obj_fn_val == 0.0 for bee in colony._bees)


def test_onlooker_keeps_role_when_accepting_better_food(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Onlookers remain onlookers after moving to better food (Karaboğa ABC)."""
    stay = 4
    colony = _colony_with_roles(
        employers=[
            Bee([0.0, 0.0], 0.0, stay, True),
            Bee([0.0, 0.0], 0.0, stay, True),
        ],
        onlookers=[
            Bee([1.0, 1.0], 2.0, stay, False),
            Bee([1.0, 1.0], 2.0, stay, False),
        ],
    )
    monkeypatch.setattr(abc_mod, "apply_mutation", lambda curr, params: [0.0, 0.0])

    colony.search()

    roles = [bee._is_employer for bee in colony._bees]
    assert roles.count(True) == 2
    assert roles.count(False) == 2
    assert all(bee._obj_fn_val == 0.0 for bee in colony._bees)
