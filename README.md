# backpack-cli

local terminal alternative to options like lighterpack

## USAGE

backpack-cli has a few top-level commands:

- list      
- add      
- remove  
- create 
- delete
- view 
- checklist 

With these, you can interact with your database.

```python
backpack list   [collections / items]   # lists items and collections
backpack add    item 1 2 --collection 4 # add items to collections
backpack remove item 4 5 --collection 6 # remove items from collections
backpack create [collection / item]
backpack delete [collection / item]
backpack view   [collection / item]
backpack checklist --collection [id]    # export a markdown checklist
```

## EXPORT

Create a markdown checklist with `backpack export [collection]`, to simplify packing and ensure you forget nothing

### ⚠️ no backwards compatibility

backpack-cli is under development, and database structure and code may change, possibly breaking compatibility.
