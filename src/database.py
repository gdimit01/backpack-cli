import sqlite3
import click
from dataobjects import Item, Collection
from typing import List, Dict

DATABASE = "backpack_cli.db"


def get_connection(database=DATABASE):
    return sqlite3.connect(database)


def get_cursor():
    conn = get_connection()
    return conn.cursor()


def get_all_items() -> List[Item]:
    cursor = get_cursor()
    cursor.execute("SELECT itemID, name, weight, note, categorie FROM item")
    items = []

    for row in cursor.fetchall():
        item_id, name, weight, note, category = row
        item = Item(item_id, name, weight, note, category)
        items.append(item)
    cursor.close
    return items


def get_item(item_id: int) -> Item:
    cursor = get_cursor()
    cursor.execute(
        "SELECT itemID, name, weight, note, categorie FROM item where itemID= ?",
        (item_id,),
    )

    row = cursor.fetchone()

    if not row:
        raise ValueError(f"Item with ID {item_id} not found")

    item_id, name, weight, note, category = row
    return Item(item_id, name, weight, note, category)


def get_collection(collection_id: int) -> Collection:
    cursor = get_cursor()

    cursor.execute(
        "SELECT collectionID, name, description FROM collection WHERE collectionID = ?",
        (collection_id,),
    )
    row = cursor.fetchone()

    if not row:
        raise ValueError(f"[red]Collection with ID {collection_id} not found[/red]")

    collection_id, name, description = row

    # Get the items associated with the collection
    cursor.execute(
        """
        SELECT i.itemID, i.name, i.weight, i.note, i.categorie
        FROM item i
        JOIN collection_items ci ON i.itemID = ci.item_id
        WHERE ci.collection_id = ?
    """,
        (collection_id,),
    )

    items = cursor.fetchall()
    # Organize items by category
    items_by_category: Dict[str, List[Item]] = {}
    for item_id, name, weight, note, category in items:
        item = Item(item_id, name, weight, note, category)
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)

    # Create and return the Collection object
    return Collection(collection_id, name, description, items_by_category)


def get_collections() -> List[Collection]:
    conn = get_connection()
    cursor = get_cursor(conn)

    # Get all collections
    cursor.execute("SELECT collectionID, name, description FROM collection")
    collections_rows = cursor.fetchall()

    collections = []

    for collection_row in collections_rows:
        collection_id, name, description = collection_row

        # Get the items associated with the collection
        cursor.execute(
            """
            SELECT i.itemID, i.name, i.weight, i.note, i.categorie
            FROM item i
            JOIN collection_items ci ON i.itemID = ci.item_id
            WHERE ci.collection_id = ?
        """,
            (collection_id,),
        )

        items = cursor.fetchall()
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
    conn = get_connection()
    cursor = get_cursor(conn)
    name = click.prompt("Enter the name of the collection", type=str)
    description = click.prompt("Enter the description of the collection", type=str)

    cursor.execute(
        "INSERT INTO collection (name, description) VALUES (?, ?)", (name, description)
    )
    conn.commit()
    conn.close()

    print(f"[green]Collection '{name}' added successfully![/green]")


def create_new_item():
    # Prompt the user for item details
    name = click.prompt("Enter the name of the item", type=str)
    weight = click.prompt("Enter the weight of the item", type=float)
    price = click.prompt("Enter the price of the item", type=float)
    category = click.prompt("Enter the category of the item", type=str)
    note = click.prompt("Enter a note for the item", type=str)

    # Insert the new item into the database
    conn = get_connection()
    cursor = get_cursor()
    cursor.execute(
        "INSERT INTO item (name, weight, categorie, note) VALUES (?, ?, ?, ?)",
        (name, weight, category, note),
    )
    conn.commit()
    conn.close()

    print(f"[green]Item '{name}' added successfully![/green]")
