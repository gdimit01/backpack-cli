import sys

import click
from rich import print
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import collection_view
from collection_view import transform_to_pie_data
from database import (
    get_items,
    get_collections,
    create_item,
    create_collection,
    get_item,
    get_collection,
    add_items_to_collection,
    delete_item,
    delete_collection,
)

console = Console()


# Click command group
@click.group()
def cli():
    pass


@cli.group()
def view():
    """View items, collections, etc."""
    pass


#  NOTE: subcommands for 'list'

@cli.group()
def list():
    """List items, collections, etc."""
    pass


@list.command()
def items():
    items = get_items()
    if items:
        print(f"\nItems in the database [dim]({len(items)})[/dim]:\n")
        for item in items:
            print(f"[dim]{item.id}:[/dim] [bold]{item.name}[/bold] [italic]{item.note}[/italic]")
        print()

    else:
        print("\n[red]No items found in the database.[/red]\n")


@list.command()
def collections():
    collections = get_collections()
    if collections:
        print(f"\nCollections in the database [dim]({len(collections)})[/dim]:\n")
        for collection in collections:
            print(
                f"[dim]{collection.id}:[/dim] [bold]{collection.name}[/bold] [italic]{collection.description}[/italic]")
        print()

    else:
        print("\n[red]No collections found in the database[/red]\n")


#  NOTE: subcommands for 'add'

@cli.group()
def add():
    """Add items, collections, etc."""
    pass


@add.command()
def item():
    name = click.prompt("Enter the name of the item", type=str)
    weight = click.prompt("Enter the weight of the item", type=float)
    category = click.prompt("Enter the category of the item", type=str)
    note = click.prompt("Enter a note for the item", type=str)

    create_item(name, weight, category, note)


@add.command()
def collection():
    name = click.prompt("Enter the name of the collection", type=str)
    description = click.prompt("Enter the description of the collection", type=str)

    create_collection(name, description)


#  NOTE: subcommands for 'view'

@view.command()
@click.argument("id", required=False, type=int)
def collection(id):
    if id is None:
        collections = get_collections()
        if collections:
            print(f"\nAvaible collections [dim]({len(collections)})[/dim]:\n")
            for collection in collections:
                print(f"[bold]{collection.id}[/bold] {collection.name}")
        else:
            click.echo("No collections found in the database")

        id = click.prompt("Enter the ID of the collection you want to view", type=int)

    try:
        collection = get_collection(id)
        view_collection(collection)
    except ValueError as e:
        click.echo(str(e))


def print_large_title(title_text):
    title = Text(title_text, style="bold white on blue")
    title.stylize("bold")  # Add underline for emphasis
    console.print(title)


def view_collection(collection):
    print_large_title(collection.name)
    print(f"[italic]{collection.description}[/italic]\n")

    data = transform_to_pie_data(collection.get_category_weights())

    print(collection_view.get_piechart(data))

    for category, items_list in collection.items.items():
        print(f"[dim]{category}[/dim]")
        print_items(items_list)
        print()


def print_items(items):
    for item in items:
        formatted_weight = collection_view.format_weight(item.weight)
        item_line = f"[bold]{item.name.ljust(20)}[/bold] [dim]Weight:[/dim] [blue]{formatted_weight.ljust(10)}[/blue] [italic]Note:[/italic] {item.note}"
        console.print(item_line)



@view.command()
@click.argument("id", required=False, type=int)
def item(id):
    if id is None:
        items = get_items()
        if items:
            click.echo("Available items:")
            for item in items:
                print(f"[dim]{item.id}:[/dim] {item.name}")
        else:
            click.echo("No items found in the database.")
            quit

        id = click.prompt("Enter the ID of the item you want to view", type=int)

    try:
        item = get_item(id)
        print(
            f"Item ID: {item.id}, Name: {item.name}, Weight: {item.weight}, Category: {item.category}"
        )
    except ValueError as e:
        click.echo(str(e))


#  NOTE: subcommands for 'delete'

@cli.group()
def delete():
    """Delete items, collections, etc."""
    pass


@delete.command()
@click.argument("id", required=False, type=int)
def item(id):
    if id is None:
        items = get_items()
        if items:
            print(f"{len(items)} available items:")
            for item in items:
                print(f"[dim]{item.id}:[/dim] {item.name}")
        else:
            print("No items found in the database.")
            sys.exit()

        id = click.prompt("Enter the ID of the item you want to delete", type=int)

    try:
        delete_item(id)
    except ValueError as e:
        click.echo(str(e))


@delete.command()
@click.argument("id", required=False, type=int)
def collection(id):
    if id is None:
        collections = get_collections()
        if collections:
            print(f"{len(collections)} available collections:")
            for collection in collections:
                print(f"[dim]{collection.id}:[/dim] {collection.name}")
        else:
            print("\nNo collections found in the database.\n")
            sys.exit()

        id = click.prompt("Enter the ID of the collection you want to delete", type=int)

    try:
        delete_collection(id)
    except ValueError as e:
        click.echo(str(e))


#  NOTE: subcommands for "collection"

@cli.group()
def collection():
    """Add and remove items to collections."""
    pass


@collection.command("add-item")
@click.argument("collection_id", type=int)
@click.argument("item_ids", nargs=-1, type=int)  # Accept multiple item_ids
def add_item_to_collection(collection_id, item_ids):
    if not item_ids:
        click.echo("You must provide at least one item ID.")
        return

    try:
        add_items_to_collection(collection_id, item_ids)
    except Exception as e:
        click.echo(f"An error occurred: {e}")


if __name__ == "__main__":
    cli()
