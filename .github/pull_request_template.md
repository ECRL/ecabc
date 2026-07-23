## Summary

<!-- What changed and why? -->

## Checklist

- [ ] Tests added or updated when behavior changes
- [ ] Docs updated if user-facing behavior or install steps change
- [ ] `[Unreleased]` entry in `CHANGELOG.md` when appropriate
- [ ] Local checks pass: `ruff check src tests`, `ruff format --check src tests`, `mypy`, `pytest`, and (if docs touched) `sphinx-build -W -b html docs/source docs/_build/html`
- [ ] Public API remains compatible per `API_STABILITY.md` (or versioning plan noted)
