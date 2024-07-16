import sys

import click
import rich
from rich.console import Console

import collection_view
from collection_view import get_pie_data
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
    remove_items_from_collection
)

from export_commands import checklist

console = Console()


# Click command group
@click.group()
def cli():
    pass


# Register the checklist command
cli.add_command(checklist)


#  NOTE: subcommands for 'add'
@cli.group()
def add():
    """Add items to collections"""
    pass


@add.command()
@click.argument('item_ids', nargs=-1, type=int, required=False)
@click.option('--collection', 'collection_id', type=int, help='Collection ID to add items to')
@click.option('--interactive', is_flag=True, help='Interactive mode to select items and collections')
def item(item_ids, collection_id, interactive):
    """
    Add items to a collection.
    """
    if interactive:
        handle_interactive_add()
    else:
        if not item_ids:
            click.echo("You must provide at least one item ID.")
            return

        if not collection_id:
            click.echo("You must provide a collection ID.")
            return

        try:
            add_items_to_collection(collection_id, item_ids)
        except Exception as e:
            click.echo(f"An error occurred: {e}")


#  NOTE: subcommands for 'add'
@cli.group()
def remove():
    """Remove items from collections"""
    pass


@remove.command()
@click.argument('item_ids', nargs=-1, type=int, required=False)
@click.option('--collection', 'collection_id', type=int, help='Collection ID to remote items from')
@click.option('--interactive', is_flag=True, help='Interactive mode to select items and collections')
def item(item_ids, collection_id, interactive):
    """
    Remove items from a collection.
    """
    if interactive:
        handle_interactive_add()
    else:
        if not item_ids:
            click.echo("You must provide at least one item ID.")
            return

        if not collection_id:
            click.echo("You must provide a collection ID.")
            return

        try:
            remove_items_from_collection(collection_id, item_ids)
        except Exception as e:
            click.echo(f"An error occurred: {e}")


@cli.group()
def view():
    """View items and collections."""
    pass


#  NOTE: subcommands for 'list'

@cli.group()
def list():
    """List items and collections."""
    pass


@list.command()
def items():
    items = get_items()
    if items:
        rich.print(f"\nItems in the database [dim]({len(items)})[/dim]:\n")
        for item in items:
            rich.print(f"[dim]{item.id}:[/dim] [bold]{item.name}[/bold] [italic]{item.note}[/italic]\n")

    else:
        rich.print("\n[red]No items found in the database.[/red]\n")


@list.command()
def collections():
    collections = get_collections()
    if collections:
        rich.print(f"\nCollections in the database [dim]({len(collections)})[/dim]:\n")
        for collection in collections:
            rich.print(
                f"[dim]{collection.id}:[/dim] [bold]{collection.name}[/bold] [italic]{collection.description}[/italic]")
        print()

    else:
        rich.print("\n[red]No collections found in the database[/red]\n")


#  NOTE: subcommands for 'add'

@cli.group()
def create():
    """Create items and collections."""
    pass


@create.command()
def item():
    name = click.prompt("Enter the name of the item", type=str)
    weight = click.prompt("Enter the weight of the item", type=float)
    category = click.prompt("Enter the category of the item", type=str)
    note = click.prompt("Enter a note for the item", type=str)

    create_item(name, weight, category, note)


@create.command()
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
            print(f"\nAvailable collections [dim]({len(collections)})[/dim]:\n")
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


def view_collection(collection):
    rich.print(f"\n≡ [bold]{collection.name}[/bold]")
    rich.print(f"  [italic]{collection.description}[/italic]\n")

    data = get_pie_data(collection.get_category_weights())

    print(collection_view.get_chart(data))
    print()

    for category, items_list in collection.items.items():
        rich.print(f"[dim]{category}[/dim]")
        print_collection_items(items_list)
        print()


def print_collection_items(items):
    for item in items:
        formatted_weight = collection_view.format_weight(item.weight)
        name = f"[bold]{item.name.ljust(20)}[/bold]"
        note = f"[italic]{item.note.ljust(40)}[/italic]"
        weight = f"[blue]{formatted_weight}[/blue]"

        rich.print(f"{name} {note} {weight}")


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
            sys.exit()

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
    """Delete items and collections."""
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
def collection(collection_id):
    if collection_id is None:
        collections = get_collections()
        if collections:
            print(f"{len(collections)} available collections:")
            for collection in collections:
                print(f"[dim]{collection.id}:[/dim] {collection.name}")
        else:
            print("\nNo collections found in the database.\n")
            sys.exit()

        collection_id = click.prompt("Enter the ID of the collection you want to delete", type=int)

    try:
        delete_collection(collection_id)
    except ValueError as e:
        click.echo(str(e))


if __name__ == "__main__":
    cli()
