# Changelog

## [UNRELEASED]
- Bumped minimum required Python version to 3.10 (previously: 3.9 which has reached end-of-life).
- Removed `version.py`, use `importlib.metadata` instead to get the version number.
- Use `uv` as a project management tool and `poe` as a task runner.
- Optimize type stubs for `Computed`, `Default` and `Rebuild` in conjunction with `ty`.
- Removed wildcard imports, so it may be necessary to change some import statements in your code when you use non-public APIs.