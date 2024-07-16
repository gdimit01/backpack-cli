# backpack-cli

local terminal alternative to options like lighterpack

## USAGE

backpack-cli has a few top-level commands:

- list *lists items and collections*
- add *add items to collections*
- remove *remove items from collections*
- create *create items and collections*
- delete *delete items and collections*
- view *view items and collections*
- checklist *export a markdown checklist*

With these, you can interact with your database.

```python
backpack list   [collections / items]
backpack add    item 1 2 --collection 4
backpack remove item 4 5 --collection 6
backpack create [collection / item]
backpack delete [collection / item]
backpack view   [collection / item]
```

## EXPORT

Create a markdown checklist with `backpack export [collection]`, to simplify packing and ensure you forget nothing

### ⚠️ no backwards compatibility

backpack-cli is under development, and database structure and code may change, possibly breaking compatibility.
