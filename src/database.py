import click
from rich import print
from dataobjects import Item, Collection, Connection
from typing import List, Dict

DATABASE = "backpack_cli.db"


def get_all_items() -> List[Item]:
    conn = Connection(DATABASE)
    conn.cursor.execute("SELECT itemID, name, weight, note, category FROM item")
    items = []

    for row in conn.cursor.fetchall():
        item_id, name, weight, note, category = row
        item = Item(item_id, name, weight, note, category)
        items.append(item)

    conn.close()
    return items


def get_item(item_id: int) -> Item:
    conn = Connection(DATABASE)
    conn.cursor.execute(
        "SELECT itemID, name, weight, note, category FROM item where itemID= ?",
        (item_id,),
    )

    row = conn.cursor.fetchone()

    if not row:
        raise ValueError(f"Item with ID {item_id} not found")

    item_id, name, weight, note, category = row

    conn.close()

    return Item(item_id, name, weight, note, category)


def get_collection(collection_id: int) -> Collection:
    conn = Connection(DATABASE)

    conn.cursor.execute(
        "SELECT collectionID, name, description FROM collection WHERE collectionID = ?",
        (collection_id,),
    )
    row = conn.cursor.fetchone()

    if not row:
        raise ValueError(f"[red]Collection with ID {collection_id} not found[/red]")

    collection_id, name, description = row

    # Get the items associated with the collection
    conn.cursor.execute(
        """
        SELECT i.itemID, i.name, i.weight, i.note, i.category
        FROM item i
        JOIN collection_items ci ON i.itemID = ci.item_id
        WHERE ci.collection_id = ?
    """,
        (collection_id,),
    )

    items = conn.cursor.fetchall()
    # Organize items by category
    items_by_category: Dict[str, List[Item]] = {}
    for item_id, name, weight, note, category in items:
        item = Item(item_id, name, weight, note, category)
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)

    return Collection(collection_id, name, description, items_by_category)


def get_collections() -> List[Collection]:
    conn =  Connection(DATABASE)

    # Get all collections
    conn.cursor.execute("SELECT collectionID, name, description FROM collection")
    collections_rows = conn.cursor.fetchall()

    collections = []

    for collection_row in collections_rows:
        collection_id, name, description = collection_row

        # Get the items associated with the collection
        conn.cursor.execute(
            """
            SELECT i.itemID, i.name, i.weight, i.note, i.category
            FROM item i
            JOIN collection_items ci ON i.itemID = ci.item_id
            WHERE ci.collection_id = ?
        """,
            (collection_id,),
        )

        items = conn.cursor.fetchall()
        # Organize items by category
        items_by_category: Dict[str, List[Item]] = {}
        for item_id, name, weight, note, category in items:
            item = Item(item_id, name, weight, note, category)
            if category not in items_by_category:
                items_by_category[category] = []
            items_by_category[category].append(item)

        # Create and add the Collection object to the list
        collection = Collection(collection_id, name, description, items_by_category)
        collections.append(collection)

    return collections


def create_collection():
    conn = Connection(DATABASE)

    name = click.prompt("Enter the name of the collection", type=str)
    description = click.prompt("Enter the description of the collection", type=str)

    conn.cursor.execute(
        "INSERT INTO collection (name, description) VALUES (?, ?)", (name, description)
    )

    conn.commit()

    print(f"[green]Collection '{name}' added successfully![/green]")


def create_new_item():
    # Prompt the user for item details
    name = click.prompt("Enter the name of the item", type=str)
    weight = click.prompt("Enter the weight of the item", type=float)
    category = click.prompt("Enter the category of the item", type=str)
    note = click.prompt("Enter a note for the item", type=str)

    # Insert the new item into the database
    conn = Connection(DATABASE)
    conn.cursor.execute(
        "INSERT INTO item (name, weight, category, note) VALUES (?, ?, ?, ?)",
        (name, weight, category, note),
    )
    conn.commit()

    print(f"\n[green]Item '{name}' added successfully![/green]\n")


def add_items_to_collection(collection_id: int, item_ids: List[int]):
    conn = Connection(DATABASE)

    for item_id in item_ids:
        conn.cursor.execute(
            "INSERT INTO collection_items (collection_id, item_id) VALUES (?, ?)",
            (collection_id, item_id),
        )

    conn.connection.commit()

    print(f"\n[green]Items added to collection {collection_id} successfully![/green]\n")

def delete_item(item_id: int):
    conn = Connection(DATABASE)

    conn.cursor.execute(
        "DELETE FROM collection_items WHERE item_id = ?", (item_id,)
    )

    conn.cursor.execute(
        "DELETE FROM item WHERE itemID = ?", (item_id,)
    )

    conn.connection.commit()
    conn.close()

    print(f"\n[green]Item with ID {item_id} was succesfully removed[/green]\n")


def delete_collection(collection_id: int):
    conn = Connection(DATABASE)

    conn.cursor.execute(
        "DELETE FROM collection_items WHERE collection_id = ?", (collection_id,)
    )

    conn.cursor.execute(
        "DELETE FROM collection WHERE collectionID = ?", (collection_id,)
    )

    conn.connection.commit()
    conn.close()

    print(f"\n[green]Collection with ID {collection_id} was succesfully removed[/green]\n")

