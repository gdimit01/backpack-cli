import sqlite3
import click
from rich import print

DATABASE = "backpack_cli.db"


def get_connection(database):
    return sqlite3.connect(database)


def get_cursor(connection):
    return connection.cursor()


# Function to get all items from the database
def get_all_items():
    conn = get_connection(DATABASE)
    cursor = get_cursor(conn)
    cursor.execute("SELECT itemID, name, weight, note FROM item")
    items = cursor.fetchall()
    conn.close()
    return items


def get_collections():
    conn = get_connection(DATABASE)
    cursor = get_cursor(conn)
    cursor.execute("SELECT name, description FROM collection")
    collections = cursor.fetchall()
    conn.close()
    return collections


def create_collection():
    conn = get_connection(DATABASE)
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
    conn = sqlite3.connect("backpack_cli.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO item (name, weight, categorie, note) VALUES (?, ?, ?, ?)",
        (name, weight, category, note),
    )
    conn.commit()
    conn.close()

    print(f"[green]Item '{name}' added successfully![/green]")


# Click command group
@click.group()
def cli():
    pass


# Group for list commands
@cli.group()
def list():
    """List items, collections, etc."""
    pass


# Group for add commands
@cli.group()
def add():
    """Add items, collections, etc."""
    pass


# Group for delete commands
@cli.group()
def delete():
    """Delete items, collections, etc."""
    pass


# Subcommands under 'list'
@list.command()
def items():
    items = get_all_items()
    if items:
        click.echo("Items in the database:")
        for item in items:
            print(f"[dim]{item[0]}:[/dim] {item[1]} {item[2]} {item[3]}")
    else:
        click.echo("No items found in the database.")


@list.command()
def collections():
    collections = get_collections()
    if collections:
        print("Collections in the database:")
        for collection in collections:
            print(f"[bold]{collection[0]}[/bold] [dim]{collection[1]}[/dim]")
    else:
        print("[red]No collections found in the database[/red]")


# Subcommands under 'add'
@add.command()
def item():
    create_new_item()


@add.command()
def collection():
    create_collection()


# Subcommands under 'delete'
@delete.command()
def item():
    # Implement deletion of an item
    pass


@delete.command()
def collection():
    # Implement deletion of a collection
    pass


if __name__ == "__main__":
    cli()
