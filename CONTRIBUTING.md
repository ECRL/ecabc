# Contributing to ECabc

Thanks for helping improve ECabc. Please read
[API_STABILITY.md](API_STABILITY.md) before changing the public surface.
Behavioral changes that affect the frozen contract need an explicit versioning
decision.

## Development setup

Requires Python 3.10+. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e ".[dev,docs]"
pre-commit install
```

## Running checks

```bash
ruff check src tests
ruff format --check src tests
mypy
pytest
sphinx-build -W -b html docs/source docs/_build/html
pre-commit run --all-files
```

`pytest` applies coverage via `pyproject.toml` (fail-under 95%).

## Documentation

Sphinx sources live under `docs/source/`. Build with the command above after
`pip install -e ".[docs]"`.

## Pull requests

- Keep the public API compatible unless the change is intentionally versioned.
- Add or update tests for behavior changes.
- Update docs when user-facing behavior or install steps change.
- Add a `[Unreleased]` entry in [CHANGELOG.md](CHANGELOG.md).
- Ensure the local checks above pass before opening the PR.

## Code of conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Releasing

Publishing is triggered by a GitHub Release (`published`) via
`.github/workflows/publish_to_pypi.yml`. The workflow currently authenticates to
PyPI with the repository secret `PYPI_API_TOKEN` (PyPI API token as
`__token__`). Prefer migrating to **PyPI trusted publishing (OIDC)** when
someone with PyPI project ownership can configure it; until then keep the token
in GitHub Actions secrets only (never commit it).

## Security

See [SECURITY.md](SECURITY.md) for private vulnerability reporting.
