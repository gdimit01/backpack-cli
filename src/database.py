from typing import List, Dict

from rich import print

from dataobjects import Item, Collection, Connection

DATABASE = "backpack_cli.db"


def get_items() -> List[Item]:
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

    print(f"[red]Item with ID {item_id} not found[/red]")

    item_id, name, weight, note, category = row

    conn.close()
    return Item(item_id, name, weight, note, category)


def get_collection(id: int) -> Collection:
    conn = Connection(DATABASE)

    conn.cursor.execute(
        "SELECT collectionID, name, description FROM collection WHERE collectionID = ?",
        (id,),
    )
    row = conn.cursor.fetchone()

    if not row:
        print(f"[red]Collection with ID {id} not found[/red]")

    id, name, description = row
    items_by_category: Dict[str, List[Item]] = get_collection_items(id)

    return Collection(id, name, description, items_by_category)


def get_collections() -> List[Collection]:
    conn = Connection(DATABASE)

    # Get all collections
    conn.cursor.execute("SELECT collectionID, name, description FROM collection")
    collections_rows = conn.cursor.fetchall()

    collections = []

    for collection_row in collections_rows:
        collection_id, name, description = collection_row
        items_by_category: Dict[str, List[Item]] = get_collection_items(collection_id)

        collection = Collection(collection_id, name, description, items_by_category)
        collections.append(collection)

    conn.close()
    return collections


def create_collection(name: str, description: str):
    conn = Connection(DATABASE)

    conn.cursor.execute(
        "INSERT INTO collection (name, description) VALUES (?, ?)", (name, description)
    )

    conn.commit()
    conn.close()

    print(f"[green]Collection '{name}' added successfully![/green]")


def get_collection_items(id):
    conn = Connection(DATABASE)
    conn.cursor.execute(
        """
        SELECT i.itemID, i.name, i.weight, i.note, i.category
        FROM item i
        JOIN collection_items ci ON i.itemID = ci.item_id
        WHERE ci.collection_id = ?
    """,
        (id,),
    )

    items = conn.cursor.fetchall()
    # Organize items by category
    items_by_category: Dict[str, List[Item]] = {}
    for item_id, name, weight, note, category in items:
        item = Item(item_id, name, weight, note, category)
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)

    conn.close()

    return items_by_category


def create_item(name: str, weight: float, category: str, note: str):
    conn = Connection(DATABASE)

    conn.cursor.execute(
        "INSERT INTO item (name, weight, category, note) VALUES (?, ?, ?, ?)",
        (name, weight, category, note),
    )
    conn.commit()
    conn.close()

    print(f"\n[green]Item '{name}' added successfully![/green]\n")


def add_items_to_collection(collection_id: int, item_ids: List[int]):
    conn = Connection(DATABASE)

    for item_id in item_ids:
        conn.cursor.execute(
            "INSERT INTO collection_items (collection_id, item_id) VALUES (?, ?)",
            (collection_id, item_id),
        )

    conn.commit()
    conn.close()

    print(f"\n[green]Items added to collection [italic]{collection_id}[/italic] successfully![/green]\n")


def delete_item(item_id: int):
    conn = Connection(DATABASE)

    # remove item from collections
    conn.cursor.execute(
        "DELETE FROM collection_items WHERE item_id = ?", (item_id,)
    )

    conn.cursor.execute(
        "DELETE FROM item WHERE itemID = ?", (item_id,)
    )

    conn.commit()
    conn.close()

    print(f"\n[green]Item with ID {item_id} was succesfully removed[/green]\n")


def delete_collection(collection_id: int):
    conn = Connection(DATABASE)

    # remove items from collection
    conn.cursor.execute(
        "DELETE FROM collection_items WHERE collection_id = ?", (collection_id,)
    )

    conn.cursor.execute(
        "DELETE FROM collection WHERE collectionID = ?", (collection_id,)
    )

    conn.commit()
    conn.close()

    print(f"\n[green]Collection with ID {collection_id} was succesfully removed[/green]\n")
