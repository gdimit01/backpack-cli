# backpack-cli

local terminal alternative to options like lighterpack

## USAGE

backpack-cli has a few top-level commands:

- list
- add
- delete

With these, you can modify objects like items, collections, etc.

#### list

```python
backpack-cli list collections
backpack-cli list items
backpack-cli list ...
```

#### add

```python
backpack-cli add collection
backpack-cli add item
backpack-cli add ...
```

#### delete

```python
backpack-cli delete collection
backpack-cli delete item
backpack-cli delete ...
```

## EXPORT

Create a markdown checklist with `backpack export [collection]`, to simplify packing and ensure you forget nothing

### ⚠️ no backwards compatibility

backpack-cli is under development, and database structure and code may change, possibly breaking compatibility.
