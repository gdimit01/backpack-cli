import sqlite3
import click

DATABASE = "backpack_cli.db"


def get_connection(database=DATABASE):
    return sqlite3.connect(database)


def get_cursor(connection=DATABASE):
    return connection.cursor()


def get_all_items():
    conn = get_connection()
    cursor = get_cursor(conn)
    cursor.execute("SELECT itemID, name, weight, note FROM item")
    items = cursor.fetchall()
    conn.close()
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


def get_collections():
    conn = get_connection()
    cursor = get_cursor(conn)
    cursor.execute("SELECT name, description FROM collection")
    collections = cursor.fetchall()
    conn.close()
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
