# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
within the compatibility policy described in [API_STABILITY.md](API_STABILITY.md).

## [Unreleased]

## [3.0.2] — 2026-07-22

API-compatible modernization release (Phases 0–4).

### Added

- `API_STABILITY.md` and Sphinx *API stability policy* page documenting the
  frozen public surface and versioning policy
- Contract and characterization test suite (`tests/test_api_contract.py`):
  signature locks, exception/warning contracts, seeded minimize-integers oracle,
  secondary-export checks, and role regressions
- `ecabc.__version__` resolved via `importlib.metadata` (packaging version
  `3.0.2` on the tip)
- Explicit package `__all__` (`ABC`, `Bee`, `Parameter`, `__version__`, `utils`)
- Optional extras: `[dev]` (pytest, coverage, ruff, mypy, pre-commit, build) and
  `[docs]` (Sphinx, Furo, autodoc type hints, copybutton)
- Sphinx + Furo documentation under `docs/source/`; `.readthedocs.yaml`
- Root `.gitignore` for Python/build/test/docs artifacts
- Ruff + pre-commit configuration; Dependabot for pip and GitHub Actions
- Governance: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
  `CITATION.cff`, issue and pull request templates
- GitHub Actions CI badge in the README

### Changed

- Package layout moved to `src/ecabc/`
- `requires-python` set to `>=3.10`; classifiers for Python 3.10–3.13; PEP 621
  license metadata
- CI: push and pull_request; lint (ruff), typecheck (mypy), and pytest matrix on
  Python 3.10–3.13; coverage fail-under 95% via `pyproject.toml`
- README installation guidance for Python 3.10+, stdlib-only runtime, and
  venv-friendly `pip install` (removed `sudo pip` / Python 2 notes)
- Publish workflow display name corrected to ECabc
- LICENSE copyright years and author list updated

### Fixed

- `ABC.search()` preserves employer/onlooker role when accepting a better
  neighboring food source (`bee_to_compare._is_employer`; Karaboğa ABC roles)
- Mutable default `obj_fn_args={}` no longer shared across `ABC` instances
  (shallow copy into instance state)
