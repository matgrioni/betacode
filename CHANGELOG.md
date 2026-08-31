# Changelog

All changes between versions will be kept track of in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Although there have been previous versions of this software, I do not think there have been previous users so this will be the first version that is kept track of.

## 1.1 - 2026-08-21
### Fixed
- The upper and lower case sequence of "h(\\|" (representing rough breathing, grave accent, and ypogegrammeni) was not actually present, and the smooth breathing version was mapped to the rough breathing unicode.

### Changed
- Ported project management from older tooling to uv

### Added
- CLI entrypoints for easier library usage
- New support for digamma characters
- Version constant in library
- More extensive tests which validate current behavior (or surface a few oddities to be fixed in later versions)
- Type annotations to public methods

## 1.0 - 2020-03-08
### Fixed
- Windows installation did not work since default encoding on Windows is CP-1252 and README read in during setup.py is encoded in UTF-8.

## 0.2 - 2018-05-25
### Added
- Use strict or non-strict mode when coverting from betacode to unicode
- Fix bug with word final sigma used when word final apostrophe after

## 0.1.6 - 2018-05-24
### Removed
- Unnecessary test file

## 0.1.5 - 2018-05-24
### Added
- Convert from betacode to unicode and back
    - Case insensitive
    - Diacritic order insensitive
    - Use oxeîa rather than tónos
- This changelog
