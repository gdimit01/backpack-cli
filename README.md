# backpack-cli

backpack-cli is a command-line tool designed for managing and organizing your collections of gear, providing a local alternative to services like Lighterpack.

![image](https://github.com/user-attachments/assets/804e2197-db11-43e9-87a6-88a6f59ee2b5)


## USAGE

With backpack-cli, you can easily interact with your database using the following commands:

list: Display a list of your collections, items, or categories.


    backpack list [collections | items | categories]

add: Add items to a collection.


    backpack add item 1 2 --collection 4

remove: Remove items from a collection.

    backpack remove item 4 5 --collection 6

create: Create a new collection or item.

    backpack create [collection | item]

delete: Delete an existing collection or item.

    backpack delete [collection | item]

view: View details of a collection or item.


    backpack view [collection | item]

checklist: Export a collection as a markdown checklist.

    backpack checklist --collection [id]

## IMPORT

Feature under development.

## EXPORT

Features under development include:

    Export to PDF
    Export to Markdown
    Export to CSV

⚠️ Note

backpack-cli is still in development. Be aware that changes to the database structure or code may affect compatibility in future updates.
