import sqlite3
import click
from rich import print


def get_connection(database):
    return sqlite3.connect(database)


def get_cursor(connection):
    return connection.cursor()


# Function to get all items from the database
def get_all_items():
    conn = get_connection("backpack_cli.db")
    cursor = get_cursor(conn)
    cursor.execute("SELECT itemID, name, weight, note FROM item")
    items = cursor.fetchall()
    conn.close()
    return items


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


# Command to retrieve and print all items
@cli.command()
def items():
    items = get_all_items()
    if items:
        click.echo("Items in the database:")
        for item in items:
            print(f"[dim]{item[0]}:[/dim] {item[1]} {item[2]} {item[3]}")
    else:
        click.echo("No items found in the database.")


# Command to create a new gear item into the database
@cli.command()
def add_item():
    create_new_item()


if __name__ == "__main__":
    cli()
