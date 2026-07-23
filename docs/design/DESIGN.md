# ECabc: API-stable modernization of an Artificial Bee Colony optimizer

**Design Document — v0.1**
**Status:** Approved (2026-07-22)
**Package:** `ecabc` (PyPI / import name unchanged)
**License:** MIT (unchanged)
**Current packaging baseline:** `3.0.1` in `pyproject.toml` (runtime `__version__` currently reports `2.2.3` — defect)
**First modernization tag:** `3.0.2` (after Phases 0–4 complete)
**Novelty review:** PROCEED — engineering modernization of an existing JOSS-published package; no new algorithm claim (see §3, §6)

---

## 1. Summary

ECabc is an open-source Python package that tunes parameters of user-supplied objective (fitness) functions using the Artificial Bee Colony (ABC) algorithm of Karaboğa. It exposes a small public surface centered on `ABC`, with supporting types `Bee` and `Parameter`, and ships with **no runtime third-party dependencies** (stdlib only). The package has a JOSS paper and downstream adoption (including historical use with ECNet for fuel-property hyperparameter tuning).

Repository engineering has partially modernized (`setup.py` → `pyproject.toml`, pytest, GitHub Actions) but still lags production-stable scientific Python practice: version drift, thin CI, missing coverage gates, no lint/typing tooling, no CHANGELOG, outdated install docs, flat layout, and a latent logic bug in an uncovered `search()` branch.

The present work modernizes packaging, testing, CI, documentation, governance, and selected internals **without changing the public API contract**. Downstream code that constructs `ABC`, calls `add_param` / `initialize` / `search`, and reads the documented properties must continue to work with identical signatures, default behaviors, return shapes, and primary exception types within the `3.0.x` / `3.1.x` compatibility series.

This document is the design source of truth for a five-phase modernization program (**Phases 0–4**).

---

## 2. Motivation and problem statement

### 2.1 Current landscape

Black-box optimization of parametric fitness functions remains a practical need in scientific computing and hyperparameter tuning. ECabc provides a pure-Python ABC implementation with optional multiprocessing. Empirically, nineteen unit tests pass and local line coverage is high (~96% when measured), but several engineering gaps limit safe maintenance:

| Area | Current state (tip / `3.0.1` packaging) |
|------|----------------------------------------|
| Public API | `ABC`, `Bee`, `Parameter`, `ecabc.utils`, `__version__` — stable in practice |
| Layout | Flat `ecabc/` package (not `src/`); ~610 LOC package + 235 LOC tests |
| Tests | Single `tests/test_all.py` (19 tests); coverage not gated in CI; private-attr heavy |
| Versioning | `pyproject.toml` `3.0.1` vs `ecabc.__version__` `2.2.3` |
| Dependencies | None at runtime (intentional) |
| Tooling | No `[dev]`/`[docs]` extras; no ruff/mypy/pre-commit; no coverage floor in CI |
| CI | Single Ubuntu + Python 3.11 job on push; Actions `@v3`; no coverage/lint |
| Docs | README tutorial + JOSS `paper/`; no Sphinx; install docs mention Python 2.7 / `sudo pip` |
| Governance | No CONTRIBUTING, CHANGELOG, CITATION.cff, SECURITY, issue/PR templates |
| Hygiene | Missing Python ignore patterns historically; publish workflow misnamed (“PaDELPy”) |
| Correctness | Suspected bug at `abc.py` employer-flag branch after mutation (`bee` vs `bee_to_compare`) |
| Publishing | Release-triggered PyPI upload via long-lived `PYPI_API_TOKEN` |

### 2.2 Why now

1. Downstream users rely on import and behavioral stability; modernization debt raises the cost of every future bugfix.
2. Version introspection already disagrees with packaging metadata — a trust and tooling failure for integrators.
3. An uncovered `search()` branch may misclassify employer/onlooker roles after accepting a better food source; fixing it requires a regression harness first.
4. A compatibility-preserving modernization is cheaper than an API rewrite that would strand notebooks, ECNet integrations, and papers citing the current API.

### 2.3 Non-goals

The following are explicitly out of scope for Phases 0–4:

1. **Changing the public API** — no renamed exports, no required new arguments, no change to return container types or primary exception types for documented failure modes.
2. **Adding hard runtime dependencies** (NumPy, SciPy, etc.) to the default install.
3. **Replacing ABC with another metaheuristic** as the default optimizer.
4. **Mandatory GPU / distributed cluster backends** beyond the existing `num_processes` multiprocessing path.
5. **JOSS resubmission** as a required deliverable (citation metadata and docs alignment are in scope; a new paper is not).
6. **Redesigning the fitness-function contract** (must remain: accept a `list` of parameter values; return a numeric value where lower is better per documented usage).
7. **Behavioral changes to colony sizing, stay limits, or default parameter names** (`P0`, `P1`, …) without a major-version plan.

---

## 3. What's genuinely new

This program is an engineering modernization of an existing scientific package, not a new optimization algorithm. Differentiation relative to a rewrite is:

1. **Frozen-contract modernization** — tooling, tests, CI, docs, and internals improve while `from ecabc import ABC` and documented methods/properties remain drop-in compatible.
2. **Characterization tests as release gates** — signature locks, exception contracts, and seeded search oracles must stay green across internal changes.
3. **Zero default Python deps preserved** — `pip install ecabc` remains stdlib-only.
4. **Production packaging baseline** — modern extras, coverage floor, multi-version CI, Sphinx, governance files, and a trustworthy release path.
5. **Explicit stability policy** — additive optional kwargs and clearer errors are allowed; intentional algorithm semantics changes require a documented version bump strategy.

---

## 4. Goals

Numbered goals are testable exit criteria for the modernization program.

1. **G1 — API contract suite.** CI fails if public signatures change or if seeded public-API characterization oracles regress beyond documented tolerances.
2. **G2 — Version and packaging.** `ecabc.__version__` matches packaging metadata (via `importlib.metadata` or equivalent single source); `[dev]` and `[docs]` extras install; `python -m build` succeeds; classifiers list supported Python versions.
3. **G3 — Correctness.** The `search()` employer-flag branch uses the bee under comparison; a dedicated regression test covers onlooker promotion paths; mutable default `obj_fn_args={}` is neutralized without changing the call signature.
4. **G4 — Tooling and quality gates.** ruff lint/format, pytest-cov with a documented coverage floor (**≥90%**, raise toward measured baseline after Phase 0), and pre-commit are enforced in CI.
5. **G5 — CI matrix.** Push/PR CI runs lint + tests on Python 3.10–3.13; coverage reported; Actions kept current.
6. **G6 — Layout.** Package lives under `src/ecabc/`; import name remains `ecabc`.
7. **G7 — Documentation.** README install docs match `requires-python`; Sphinx site with install + API autodoc builds with warnings as errors; JOSS paper remains cited.
8. **G8 — Governance.** CONTRIBUTING, CHANGELOG, CITATION.cff, SECURITY, CODE_OF_CONDUCT, and issue/PR templates present; LICENSE copyright includes all authors.
9. **G9 — Release path.** Publish workflow correctly named for ECabc; prefer trusted publishing (OIDC) when credentials allow; tag **`3.0.2`** only after Phases 0–4 exit criteria pass.

---

## 5. Target users and use cases

| User | Use case |
|------|----------|
| Scientific Python practitioner | Minimize/maximize a custom fitness function over bounded parameters |
| Hyperparameter tuner | Wrap a model-training objective and search integer/float hyperparameters |
| Library integrator | Depend on `ecabc` as a stable PyPI dependency without adapting to API churn |
| Maintainer / contributor | Run lint/tests locally and in CI; cut safe patch releases with changelog discipline |

**Primary constraint:** integrators must not need code changes when upgrading within the `3.0.x` / `3.1.x` compatibility series.

---

## 6. Related work

| Project | What it does | Status | Gap this package fills |
|---------|--------------|--------|------------------------|
| Karaboğa ABC (Scholarpedia / original papers) | Foundational ABC metaheuristic | Canonical algorithm literature | ECabc is a small, dependency-free Python implementation for user fitness functions |
| [scipy.optimize](https://docs.scipy.org/doc/scipy/reference/optimize.html) | Broad SciPy optimization suite | Mature | Heavier dependency; different API; not an ABC-focused minimal tuner |
| [pymoo](https://pymoo.org/) | Multi-objective evolutionary optimization | Active | Larger framework; different API and dependency stack |
| [Nevergrad](https://facebookresearch.github.io/nevergrad/) | Gradient-free optimization toolbox | Active | Broader scope; not a drop-in for existing `ecabc` callers |
| [mealpy](https://github.com/thieu1995/mealpy) | Large metaheuristic collection including ABC | Active | Different API; migrating would break existing ECabc callers |

**Primary literature (cite in docs/tests where the algorithm is discussed):**

- Karaboğa D. An idea based on honey bee swarm for numerical optimization. Technical Report TR06, Erciyes University, 2005.
- Karaboğa D. Artificial bee colony algorithm. *Scholarpedia*, 5(3):6915, 2010.
- JOSS paper for this package: DOI [10.21105/joss.01420](https://doi.org/10.21105/joss.01420).

---

## 7. Architecture overview

ECabc remains a **thin layered optimizer**. Modernization may refine helpers and packaging layout but must preserve the import surface.

```text
┌─────────────────────────────────────────────────────────┐
│  Public API (ecabc.__init__)                            │
│  ABC, Bee, Parameter, utils, __version__                │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  L2 Colony orchestration — ecabc.abc.ABC                │
│  add_param, initialize, search, best_*/average_* props  │
│  multiprocessing Pool for objective evaluations         │
└───────────────────────────┬─────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────────┐
│ L1 Bee        │   │ L1 Parameter  │   │ L1 utils          │
│ solution +    │   │ bounds,       │   │ mutate, choose,   │
│ fitness, stay │   │ mutate, rand  │   │ call_obj_fn, best │
└───────────────┘   └───────────────┘   └───────────────────┘
```

**Dependency rule:** `abc` may import `bee`, `parameter`, and `utils`; `bee` / `parameter` / `utils` must not import `abc`. New helpers stay private unless deliberately re-exported.

**Layout decision:** Migrate to `src/ecabc/` in **Phase 2**. The import name remains `import ecabc`.

---

## 8. Core data model and public API

### 8.1 Frozen public surface

```python
from ecabc import ABC, Bee, Parameter
import ecabc.utils
from ecabc import __version__
```

Primary documented workflow (signatures and defaults must remain compatible; additive optional kwargs only):

```python
def __init__(
    self,
    num_employers: int,
    objective_fn: Callable[[list], float],
    obj_fn_args: dict = {},   # signature preserved; implement as None + copy internally
    num_processes: int = 1,
) -> None: ...

def add_param(
    self,
    min_val: int | float,
    max_val: int | float,
    restrict: bool = True,
    name: str | None = None,
) -> None: ...

def initialize(self) -> None: ...
def search(self) -> None: ...

@property
def best_fitness(self) -> float: ...
@property
def best_ret_val(self) -> int | float | None: ...
@property
def best_params(self) -> dict: ...
@property
def average_fitness(self) -> float | None: ...
@property
def average_ret_val(self) -> float | None: ...
```

### 8.2 Objective-function contract

| Rule | Contract |
|------|----------|
| Input | A `list` of parameter values (`int` and/or `float`) |
| Output | Numeric objective value |
| Sense | Lower return values are better (per README / examples) |
| Extra args | Via `obj_fn_args` kwargs dict passed through to the objective |

### 8.3 Exception and warning contracts (preserve)

| Condition | Type |
|-----------|------|
| Non-callable objective | `ReferenceError` |
| `add_param` after `initialize` | `RuntimeError` |
| `search` before `initialize` | `RuntimeError` |
| Second `initialize` | `RuntimeWarning` |
| Parameter min/max type mismatch | `ValueError` |

### 8.4 Behavioral invariants (do not change without major version)

1. After `initialize`, colony size is `2 × num_employers` (employers + onlookers).
2. Stay limit is `num_employers × num_parameters`.
3. Default keys in `best_params` are `P0`, `P1`, … when `name` is omitted.
4. Fitness transform remains `Bee.calc_fitness` semantics (`1/(1+ofv)` if `ofv >= 0`, else `1 + abs(ofv)`).

### 8.5 Secondary exports

`Bee`, `Parameter`, and `ecabc.utils` (`apply_mutation`, `call_obj_fn`, `choose_bee`, `determine_best_bee`) remain importable. Tests today use them; downstream may as well. Modernization must not remove these symbols. Explicit `__all__` may be added listing the intentional public names.

### 8.6 Stability policy

1. **Patch (`3.0.x`):** bugfixes, tooling, packaging, docs, and internal hardening that preserve the frozen API. This modernization program ships as **`3.0.2`** after Phases 0–4.
2. **Minor (`3.1.0` and later):** reserved for future additive, still API-compatible work after `3.0.2`.
3. **Major (`4.0.0` or higher):** only after an explicit stability/migration plan (e.g. intentional algorithm semantics change or API redesign).

---

## 9. Module design

### 9.1 `ecabc` (`__init__.py`)

**Purpose:** Re-export the public API and `__version__`.
**Changes:** Sync version from packaging metadata; add explicit `__all__`; keep exporting `ABC`, `Bee`, `Parameter`, and `utils`.

### 9.2 `ecabc.abc`

**Purpose:** Colony lifecycle and search cycles.
**Key behaviors to preserve:** employer/onlooker initialization; mutation evaluation; abandon/scout paths; multiprocessing via `num_processes`; property accessors.
**Internal improvements:**
- Phase 1: fix employer-flag branch to use `bee_to_compare._is_employer`; neutralize mutable default args; prefer `with Pool(...)` lifecycle without changing API.
- Phase 2+: typing cleanup that does not alter runtime behavior.

### 9.3 `ecabc.bee`

**Purpose:** Per-solution state (parameters, objective value, fitness, stay count, employer flag).
**Preserve:** constructor signature; `abandon` side effect; `calc_fitness`; `is_better_food`.

### 9.4 `ecabc.parameter`

**Purpose:** Search-space bounds and mutation.
**Preserve:** type checks; `restrict` behavior; `rand_val`; `mutate`.

### 9.5 `ecabc.utils`

**Purpose:** Mutation application, objective invocation, probabilistic bee selection, best-bee determination.
**Preserve:** function names and return shapes used by `ABC` and existing tests.

---

## 10. Dependencies and ecosystem integration

| Kind | Decision |
|------|----------|
| Runtime Python deps | None (stdlib only) |
| Optional extras | `[dev]` — pytest, pytest-cov, ruff, mypy, pre-commit, build; `[docs]` — Sphinx, Furo, autodoc stack |
| Ecosystem | Remains usable from notebooks and from packages such as ECNet without import changes |
| Multiprocessing | Continues to use stdlib `multiprocessing`; document Windows spawn considerations if needed |

No NumPy/SciPy hard dependency will be introduced in the default install during Phases 0–4.

---

## 11. Validation strategy

### 11.1 Phase 0 — Contract suite (load-bearing)

| Test class | What | Pass criteria |
|------------|------|---------------|
| Signature locks | `inspect.signature` for `ABC.__init__`, `add_param`, `initialize`, `search` | Parameter names + defaults match frozen contract |
| Property smoke | Public properties after `initialize` / `search` | Types/shapes match contract; no private-attr requirement |
| Exception contracts | Non-callable obj; search before init; add_param after init; bad Parameter types | Exact exception types |
| Seeded characterization | Fixed `random.seed` / controlled RNG where feasible; minimize-integers style objective | Colony size, stay limit, and monotonic-or-stable best objective over N cycles within documented oracle |
| Secondary API | `Bee.calc_fitness`, `Parameter.mutate` bounds, utils helpers | Existing behavioral expectations locked |

Store oracles under `tests/` (optionally `tests/fixtures/`) with a short note that they are **API characterization** references for the compatibility series, not independent literature tables (unless later expanded).

### 11.2 Phase 1 — Correctness regressions

| Test class | What | Pass criteria |
|------------|------|---------------|
| Employer-flag regression | Construct a scenario where an onlooker accepts a better mutated food source | New bee retains onlooker role (`is_employer=False`); employers retain employer role |
| Mutable default isolation | Two `ABC` instances mutate `obj_fn_args` independently after using default | No cross-instance leakage |
| Re-initialize warning | Second `initialize` | `RuntimeWarning` |

### 11.3 Unit vs integration

- **Unit:** Parameter mutation bounds, fitness calc, utils selection, signature locks (no multi-cycle search required).
- **Integration / characterization:** Multi-cycle `search()` with and without `num_processes>1` (keep multiprocessing coverage; mark slow if needed).

### 11.4 Coverage

- CI floor from Phase 3 onward: **≥90%** line coverage on package modules (`src/ecabc/**/*.py` after layout migration; `ecabc/**/*.py` before).
- Raise the floor toward the measured ~96% baseline once Phase 0–1 tests land, if stable.

### 11.5 Docs / examples

- Keep `examples/minimize_integers.py` working without API changes.
- Sphinx `-W` build in CI after Phase 4.
- Notebooks are optional; not a Phase 0–3 blocker.

### 11.6 Local verification and CI gates

**Local-first (Phases 0–4):** All phase work must be completed and verified **locally** before any push intended for release. Local commands are the definition of done for each phase exit (lint, tests + coverage, docs build once Sphinx exists, `python -m build` when packaging is in scope).

**Remote CI (release branch):** Repository CI (lint + test matrix + docs when present) runs when changes are pushed. That push is a confirmation gate after local verification, not a substitute for it.

---

## 12. Open-source packaging

| Concern | Decision |
|---------|----------|
| Build backend | setuptools via `pyproject.toml` (current); keep unless a zero-risk hatchling migration is approved later |
| Layout | `src/ecabc/` in Phase 2 |
| Python versions | `requires-python = ">=3.10"`; CI on 3.10, 3.11, 3.12, 3.13 |
| License | MIT; update copyright line to include all authors |
| Docs | Sphinx + Furo under `docs/source/`; Read the Docs config; keep JOSS `paper/` in repo (exclude from wheels as today) |
| CI | Replace thin test workflow with lint + pytest matrix; keep/repair publish workflow name |
| Release | Tag-triggered publish; prefer PyPI trusted publishing (OIDC) |
| Governance | CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, SECURITY, issue/PR templates |
| Citation | `CITATION.cff` pointing at the GitHub repo and JOSS DOI |
| Supply chain | Current Actions majors or SHA pins + Dependabot; no secrets in repo |

---

## 13. Roadmap (Phases 0–4)

Phases map to implementation milestones. The sole PyPI tag for this program is **`3.0.2`**, cut at the end of **Phase 4** after Phases 0–3 exit. Intermediate work stays on the tip without interim tags. **All Phases 0–4 work must be done and verified locally** (§11.6).

| Phase | Theme | Primary goals | Suggested version |
|-------|-------|---------------|-------------------|
| **0** | Freeze the contract | G1 — signatures, public-API oracles, exception contracts | Commits on tip (no tag) |
| **1** | Correctness & metadata | G2 (partial), G3 — version sync, search bug fix, hygiene, README install fix | Commits on tip (no tag) |
| **2** | Packaging hygiene | G2, G6 — `src/` layout, extras, `__all__`, license metadata | Commits on tip (no tag) |
| **3** | CI & quality gates | G4, G5 — ruff/mypy/pre-commit, coverage gate, 3.10–3.13 matrix | Commits on tip (no tag) |
| **4** | Docs, governance, release | G7, G8, G9 — Sphinx, governance files, publish path, tag **`3.0.2`** | Tag **`3.0.2`** |

### 13.1 Phase 0 — Freeze the contract

**Intent:** Make unsafe refactors detectable before correctness and layout moves.

Deliverables:

1. Document the frozen API (this design §8; optionally a short `API_STABILITY.md` migrated into Sphinx in Phase 4).
2. Add public-API-only characterization tests (signature locks, exception contracts, seeded minimize-integers style oracle).
3. Record coverage baseline with `pytest-cov` (informational in Phase 0; gated in Phase 3).
4. Prefer tests that do not require private attributes (`_bees`, `_params`) for the contract suite; existing private-attr tests may remain temporarily.

**Exit:** Local `pytest` green; contract suite present; coverage baseline noted in the PR/description.

### 13.2 Phase 1 — Correctness & metadata

**Intent:** Fix trust-breaking defects and repository hygiene without changing the public API.

Deliverables:

1. Single-source version: packaging and `ecabc.__version__` agree (prefer `importlib.metadata.version("ecabc")` with a safe editable-install fallback if needed). Recommendation: set packaging version to `3.0.2` when the bug fix lands; publish only in Phase 4.
2. Fix `search()` employer-flag branch (`bee_to_compare._is_employer`) with regression test (§11.2).
3. Neutralize mutable default `obj_fn_args` while preserving the signature.
4. Ensure root `.gitignore` covers Python/build/test artifacts.
5. Rename publish workflow from PaDELPy to ECabc; audit for other copy-paste errors.
6. Update README install section for Python ≥3.10; remove `sudo pip` / Python 2.7 guidance; add CI badge.
7. Start `CHANGELOG.md` (Keep a Changelog); update LICENSE copyright authors.

**Exit:** Version strings agree; bug regression green; README install accurate; hygiene files present.

### 13.3 Phase 2 — Packaging hygiene

**Intent:** Bring packaging layout and metadata to current norms without algorithm rewrites.

Deliverables:

1. Migrate to `src/ecabc/`; configure setuptools `where = ["src"]`; verify `import ecabc` from an editable/wheel install (not merely the source tree).
2. Add `[project.optional-dependencies]` for `dev` and `docs`.
3. Add PEP 621 `license` field; expand classifiers to 3.10–3.13 (as CI will cover in Phase 3).
4. Add `__all__` to `__init__.py`.
5. Keep `paper*` excluded from wheels.

**Exit:** Locally, `pip install -e ".[dev]"` works; tests collect against the installed package; build produces sdist/wheel that import cleanly.

### 13.4 Phase 3 — CI & quality gates

**Intent:** Enforce quality on every push/PR.

Deliverables:

1. CI matrix: Python 3.10–3.13 on `ubuntu-latest` (optional macOS later).
2. Lint job: ruff check + format check; mypy (start non-blocking if needed, then required).
3. Test job: pytest with `--cov=ecabc --cov-fail-under=90` (or higher if baseline allows).
4. Restore `.pre-commit-config.yaml` with ruff (and mypy if stable).
5. Bump Actions to current majors (or SHA-pin); add Dependabot for Actions.
6. Split `tests/test_all.py` by module when convenient (optional if contract suite already structured).

**Exit:** Local ruff + pytest+cov pass; workflow files correct for the matrix; pre-commit passes on touched files.

### 13.5 Phase 4 — Docs, governance, and compatibility release (`3.0.2`)

**Intent:** Make the project maintainable and ship the modernization.

Deliverables:

1. Sphinx + Furo under `docs/source/` with install + API autodoc; `.readthedocs.yaml`; `sphinx-build -W` clean.
2. Governance: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CITATION.cff, issue/PR templates; CHANGELOG finalized for `3.0.2`.
3. Confirm Phases 0–3 are **locally verified** (lint, tests + coverage, docs `-W`, build) per §11.6.
4. Refresh publish workflow (prefer trusted publishing / OIDC if credentials allow; otherwise document token path).
5. Set version to **`3.0.2`**, tag, and publish only after local verification (and after release-branch CI is green when that push is used).
6. Post-release: monitor issues; plan future `3.1.0` / `4.0.0` only with explicit scope (out of scope for this program).

**Exit (`3.0.2`):** Phases 0–4 done and verified locally; PyPI artifact installable; contract suite passes on the release commit from a clean venv.

```mermaid
flowchart LR
  P0[Phase 0 Contract] --> P1[Phase 1 Correctness]
  P1 --> P2[Phase 2 Packaging]
  P2 --> P3[Phase 3 CI Gates]
  P3 --> P4[Phase 4 Docs and Release]
  P0 -.->|oracles gate every later phase| P1
  P0 -.->|oracles gate release| P4
```

---

## 14. Open questions

### 14.1 Resolved (2026-07-22)

| # | Decision |
|---|----------|
| Q1 | Migrate to `src/ecabc/` in **Phase 2**. |
| Q2 | Tag **`3.0.2`** once after Phases 0–4; no interim tags. |
| Q3 | Initial coverage floor is **90%** on package modules; raise if stable after Phase 0–1. |
| Q4 | mypy may start non-blocking in Phase 3; make required before `3.0.2` if feasible. |
| Q5 | Prefer PyPI trusted publishing (OIDC) in Phase 4 when credentials allow. |
| Q9 | Support **Python 3.10+** (`requires-python = ">=3.10"`; CI on 3.10–3.13). |

### 14.2 Still open (non-blocking)

| # | Question | Options | Recommendation | Owner |
|---|----------|---------|----------------|-------|
| Q6 | Enable macOS/Windows CI runners? | Ubuntu-only vs multi-OS | Ubuntu required for `3.0.2`; add macOS later if multiprocessing spawn issues appear | Maintainer |
| Q7 | Should `restrict=False` end-to-end search be part of Phase 0 oracles? | Phase 0 vs Phase 1 | Include a minimal Phase 0/1 test; not a release blocker if coverage already hits the branch | Maintainer |
| Q8 | Keep exporting `ecabc.utils` as a module attribute forever? | Freeze vs soft-deprecate in docs only | Freeze for `3.x`; document as secondary API | Maintainer |

---

## Appendix A — Mapping audit findings to phases

| Finding | Phase |
|---------|-------|
| No public-API-only contract suite; private-attr-heavy tests | 0 |
| Version mismatch `3.0.1` vs `2.2.3` | 1 |
| Suspected `search()` employer-flag bug (`abc.py`) | 1 |
| Mutable default `obj_fn_args={}` | 1 |
| Publish workflow named PaDELPy; README Python 2 / sudo pip | 1 |
| Flat layout; no optional-deps; no `__all__` | 2 |
| Single-Python CI; no ruff/mypy/coverage gate; no pre-commit | 3 |
| No Sphinx/RTD; no CHANGELOG/governance/citation | 4 |
| Long-lived PyPI token | 4 |
| NumPy/SciPy rewrite pressure | Explicit non-goal |

## Appendix B — Approval checklist

- [x] Maintainer approves API freeze and non-goals (§2.3, §8)
- [x] Maintainer answers Q1–Q5 (src layout; tag `3.0.2`; 90% coverage; mypy policy; OIDC)
- [x] Design accepted → create implementation blueprint
- [x] Execute Phase 0 first (contract suite / signature locks)
- [x] No implementation of Phases 2–4 until Phase 0 oracles exist (recommended gate)
- [x] Phase 1 bug fix merges only with its regression test
- [ ] All Phases 0–4 work done and verified locally before release push (§11.6)
- [ ] Tag `3.0.2` only when Phases 0–3 exit criteria pass and Phase 4 release checklist is complete
