# backpack-cli

local terminal alternative to options like lighterpack

## USAGE

backpack-cli has a few top-level commands:

- list
- add
- delete
- view

With these, you can modify objects like items, collections, etc.

```python
backpack-cli list [collections / items]
backpack-cli add [collection / item]
backpack-cli delete [collection / item]
backpack-cli view [collection / item]
```

## EXPORT

Create a markdown checklist with `backpack export [collection]`, to simplify packing and ensure you forget nothing

### ⚠️ no backwards compatibility

backpack-cli is under development, and database structure and code may change, possibly breaking compatibility.
