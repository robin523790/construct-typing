# Changelog

## [UNRELEASED]
** Breaking changes: **
- `csfield` should only used for constructs that cannot build from `None`. Every other construct should use the new `csfield_noinit`, `csfield_const` or `csfield_default`.
- Removed wildcard imports, so it may be necessary to change some import statements in your code when you use non-public APIs.
- Bumped minimum required Python version to 3.10 (previously: 3.9 which has reached end-of-life).
- Removed `version.py`, use `importlib.metadata` instead to get the version number.

** New features: **
- Added `csfield_const` to create dataclass fields that are excluded from constructor and have a constant value.
- Added `csfield_default` to create dataclass fields that have a default value.
- Added `csfield_noinit` to create dataclass fields that are excluded from constructor.
- Optimize type stubs for `Computed`, `Default` and `Rebuild` in conjunction with `ty`.
- Optimize type stubs for `Checksum`, to represent that it can build from `None`.

** Organizational changes: **
- Use `uv` as a project management tool and `poe` as a task runner.