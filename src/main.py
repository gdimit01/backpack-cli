import sqlite3
import click


# Function to get all items from the database
def get_all_items():
    conn = sqlite3.connect("backpack_cli.db")  # Connect to your SQLite database
    cursor = conn.cursor()
    cursor.execute("SELECT itemID, name, weight, note FROM item")
    items = cursor.fetchall()
    conn.close()
    return items


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
            click.echo(f"{item[0]}: {item[1]} {item[2]} {item[3]}")
    else:
        click.echo("No items found in the database.")


if __name__ == "__main__":
    cli()
