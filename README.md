# backpack-cli

<!-- README.md -->
+ [![cov](https://https://kaya-sem.github.io/backpack-cli//badges/coverage.svg)](https://github.com/Kaya-Sem/backpack-cli/actions)

local terminal alternative to options like lighterpack

## USAGE

backpack-cli has a few top-level commands:

- list
- add
- delete
- view

With these, you can modify objects like items, collections, etc.

```python
backpack list [collections / items]
backpack add [collection / item]
backpack delete [collection / item]
backpack view [collection / item]
```

## EXPORT

Create a markdown checklist with `backpack export [collection]`, to simplify packing and ensure you forget nothing

### ⚠️ no backwards compatibility

backpack-cli is under development, and database structure and code may change, possibly breaking compatibility.
