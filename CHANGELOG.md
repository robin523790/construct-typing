# Changelog

## [UNRELEASED]
- Bumped minimum required Python version to 3.10 (previously: 3.9 which has reached end-of-life).
- Removed `version.py`, use `importlib.metadata` instead to get the version number.
- Use `uv` as a project management tool and `poe` as a task runner.