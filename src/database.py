from typing import List, Dict
from collection import print_collections
from item import print_items
import click

import rich
from dataobjects import Item, Collection, Connection

DATABASE = "backpack_cli.db"


def get_items() -> List[Item]:
    conn = Connection(DATABASE)
    conn.cursor.execute("SELECT id, name, weight, note, category FROM items")
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
        "SELECT id, name, weight, note, category FROM items where id= ?",
        (item_id,),
    )

    row = conn.cursor.fetchone()

    if row:
        item_id, name, weight, note, category = row
        conn.close()
        return Item(item_id, name, weight, note, category)
    else:
        print(f"[red]Item with ID {item_id} not found[/red]")
        conn.close()


def get_collection(id: int) -> Collection:
    conn = Connection(DATABASE)

    conn.cursor.execute(
        "SELECT id, name, description FROM collections WHERE id = ?",
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
    conn.cursor.execute("SELECT id, name, description FROM collections")
    collections_rows = conn.cursor.fetchall()

    collections = []

    for collection_row in collections_rows:
        collection_id, name, description = collection_row
        items_by_category: Dict[str, List[Item]] = get_collection_items(collection_id)

        collection = Collection(collection_id, name, description, items_by_category)
        collections.append(collection)

    conn.close()
    return collections


def create_collection(name: str, description: str) -> int:
    conn = Connection(DATABASE)

    conn.cursor.execute(
        "INSERT INTO collections (name, description) VALUES (?, ?)", (name, description)
    )

    collection_id = conn.cursor.lastrowid

    conn.commit()
    conn.close()

    return collection_id


def get_collection_items(id):
    conn = Connection(DATABASE)
    conn.cursor.execute(
        """
        SELECT i.id, i.name, i.weight, i.note, i.category
        FROM items i
        JOIN collection_items ci ON i.id = ci.item_id
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


# creates item in database and returns it generated id.
def create_item(name: str, weight: int, category: str, note: str) -> int:
    conn = Connection(DATABASE)

    conn.cursor.execute(
        "INSERT INTO items (name, weight, category, note) VALUES (?, ?, ?, ?)",
        (name, weight, category, note),
    )

    item_id = conn.cursor.lastrowid

    conn.commit()
    conn.close()

    return item_id


def get_collection_items_as_list(collection_id: int) -> List[Item]:
    conn = Connection(DATABASE)

    conn.cursor.execute(
        """
        SELECT i.id, i.name, i.weight, i.note, i.category
        FROM items i
        JOIN collection_items ci ON i.id = ci.item_id
        WHERE ci.collection_id = ?
    """,
        (collection_id,),
    )

    items_rows = conn.cursor.fetchall()
    items = [Item(item_id, name, weight, note, category) for item_id, name, weight, note, category in items_rows]

    conn.close()

    return items


def remove_items_from_collection(collection_id: int, item_ids: List[int]):
    conn = Connection(DATABASE)

    removed_count = 0
    skipped_count = 0

    for item_id in item_ids:
        # Check if the item is present in the collection
        conn.cursor.execute(
            "SELECT COUNT(*) FROM collection_items WHERE collection_id = ? AND item_id = ?",
            (collection_id, item_id),
        )
        exists = conn.cursor.fetchone()[0]

        if exists:
            conn.cursor.execute(
                "DELETE FROM collection_items WHERE collection_id = ? AND item_id = ?",
                (collection_id, item_id),
            )
            removed_count += 1
        else:
            skipped_count += 1

    conn.commit()
    conn.close()

    if removed_count > 0:
        rich.print(
            f"\n[green]{removed_count} item(s) removed from collection [italic]{collection_id}[/italic] "
            f"successfully![/green]")
    if skipped_count > 0:
        rich.print(f"\n[yellow]{skipped_count} item(s) were not in the collection and were skipped.[/yellow]\n")


def add_items_to_collection(collection_id: int, item_ids: List[int]):
    if collection_id is None or item_ids is None:
        print("Error!")
        raise Exception

    conn = Connection(DATABASE)

    added_count = 0
    skipped_count = 0

    for item_id in item_ids:
        # Check if the item is already in the collection
        conn.cursor.execute(
            "SELECT COUNT(*) FROM collection_items WHERE collection_id = ? AND item_id = ?",
            (collection_id, item_id),
        )
        exists = conn.cursor.fetchone()[0]

        if exists:
            skipped_count += 1
        else:
            conn.cursor.execute(
                "INSERT INTO collection_items (collection_id, item_id) VALUES (?, ?)",
                (collection_id, item_id),
            )
            added_count += 1

    conn.commit()
    conn.close()

    if added_count > 0:
        rich.print(
            f"\n[green]{added_count} item(s) added to collection [italic]{collection_id}[/italic] successfully![/green]")
    if skipped_count > 0:
        rich.print(f"\n[yellow]{skipped_count} item(s) were already in the collection and were skipped.[/yellow]\n")


def delete_item(item_id: int):
    conn = Connection(DATABASE)

    #  TODO: items should not be removed, rather 'archived'
    # remove item from collections
    conn.cursor.execute(
        "DELETE FROM collection_items WHERE item_id = ?", (item_id,)
    )

    conn.cursor.execute(
        "DELETE FROM items WHERE id = ?", (item_id,)
    )

    conn.commit()
    conn.close()

    rich.print(f"\n[green]Item with ID {item_id} was succesfully removed[/green]\n")


def delete_collection(collection_id: int):
    conn = Connection(DATABASE)

    # remove items from collection
    conn.cursor.execute(
        "DELETE FROM collection_items WHERE collection_id = ?", (collection_id,)
    )

    conn.cursor.execute(
        "DELETE FROM collections WHERE id = ?", (collection_id,)
    )

    conn.commit()
    conn.close()


def get_categories() -> List[str]:
    conn = Connection(DATABASE)
    conn.cursor.execute("SELECT DISTINCT category FROM items")
    categories = [row[0] for row in conn.cursor.fetchall()]
    conn.close()

    return categories


def handle_interactive_add():
    rich.print(f"\n[underline]Choose a collection to add items to:[/underline]\n")

    collections = get_collections()
    print_collections(collections)

    print()
    collection_id = click.prompt("Collection ID", type=int)

    items = get_items()
    rich.print(f"\n[underline]Choose items to add to a collection:[/underline]\n")
    print_items(items)

    rich.print(f"\nSeparate IDs with spaces")
    response = click.prompt("Item IDs")

    # Convert the response string into a list of integers
    try:
        item_ids = [int(item_id) for item_id in response.split()]
    except ValueError:
        print(f"\n[red]Invalid input. Please enter numbers separated by spaces.[/red]\n")
        return

    add_items_to_collection(collection_id, item_ids)


#  TODO: check if there's actually any items in the collection
def handle_interactive_remove():
    rich.print(f"\n[underline]Choose a collection to remove items from:[/underline]\n")

    collections = get_collections()
    print_collections(collections)

    print()

    collection_id = click.prompt("Collection ID", type=int)
    print()

    rich.print(f"\n[underline]Choose items to add to a collection:[/underline]\n")
    items = get_collection_items_as_list(collection_id)
    print_items(items)

    print(f"\nSeparate IDs with spaces")
    response = click.prompt("Item IDs")

    # Convert the response string into a list of integers
    try:
        item_ids = [int(item_id) for item_id in response.split()]
    except ValueError:
        rich.print(f"\n[red]Invalid input. Please enter numbers separated by spaces.[/red]\n")
        return

    remove_items_from_collection(collection_id, item_ids)
