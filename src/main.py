import sys

import click
import rich
from rich.console import Console

from item import print_items
from collection import print_collections, print_collection_view
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
    remove_items_from_collection,
    handle_interactive_add,
    get_categories,
    handle_interactive_remove
)
from export_commands import checklist
from dataobjects import Collection

console = Console()


# Click command group
@click.group()
def cli():
    pass


# Register the sourced checklist command
cli.add_command(checklist)


#  NOTE: subcommands for 'add'
@cli.group()
def add():
    """Add items to collections"""
    pass


@add.command()
@click.argument('item_ids', nargs=-1, type=int, required=False)
@click.option('-c', '--collection', 'collection_id', type=int, help='Collection ID to add items to')
@click.option('-i', '--interactive', is_flag=True, help='Interactive mode to select items and collections')
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
@click.option('-c', '--collection', 'collection_id', type=int, help='Collection ID to remote items from')
@click.option('-i', '--interactive', is_flag=True, help='Interactive mode to select items and collections')
def item(item_ids, collection_id, interactive):
    """
    Remove items from a collection.
    """
    if interactive:
        handle_interactive_remove()
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
    """List items, collections and categories"""
    pass


@list.command()
def items():
    items = get_items()
    if items:
        rich.print(f"\nItems in the database [dim]({len(items)})[/dim]:\n")
        print_items(items)

    else:
        rich.print("\n[red]No items found in the database.[/red]\n")


@list.command()
def categories():
    categories = get_categories()
    if categories:
        console.print("\nCategories in the database:\n")
        for category in categories:
            console.print(f"- {category}")
    else:
        console.print("\n[red]There are no categories in the database.[/red]\n")


@list.command()
def collections():
    collections = get_collections()
    if collections:
        rich.print(f"\nCollections in the database [dim]({len(collections)})[/dim]:\n")
        print_collections(collections)
        print()

    else:
        rich.print("\n[red]No collections found in the database[/red]\n")


#  NOTE: subcommands for 'add'

@cli.group()
def create():
    """Create items and collections."""
    pass


#  TODO: named arguments
@create.command()
def item():
    name = click.prompt("Enter the name of the item", type=str)
    weight = click.prompt("Enter the weight of the item", type=int)
    category = click.prompt("Enter the category of the item", type=str)
    note = click.prompt("Enter a note for the item", type=str)

    item_id = create_item(name, weight, category, note)

    if item_id:
        rich.print(f"\n[green]Item '{name}' added successfully with ID {item_id}![/green]\n")
    else:
        rich.print(f"\n[red]Item '{name}' could not be added![/red]\n")


@create.command()
@click.option('-n', '--name', type=str, help='Name of the collection')
@click.option('-d', '--description', type=str, help='Description of the collection')
@click.option('-i', '--interactive', is_flag=True, help='Interactive mode')
def collection(name, description, interactive):
    if interactive:
        name = click.prompt("Enter the name of the collection", type=str)
        description = click.prompt("Enter the description of the collection", type=str)
    elif not name or not description:
        raise click.UsageError("In non-interactive mode, both --name and --description must be provided.")

    collection_id = create_collection(name, description)

    rich.print(f"[green]Collection '{name}' with ID {collection_id} was created successfully![/green]")


#  NOTE: subcommands for 'view'

@view.command()
@click.argument("id", required=False, type=int)
def collection(id):
    if id is None:
        collections = get_collections()
        if collections:
            rich.print(f"\nAvailable collections [dim]({len(collections)})[/dim]:\n")
            print_collections(collections)
        else:
            click.echo("No collections found in the database")

        id = click.prompt("Enter the ID of the collection you want to view", type=int)

    try:
        col: Collection = get_collection(id)
        print_collection_view(col)
    except ValueError as e:
        click.echo(str(e))


@view.command()
@click.argument("id", required=False, type=int)
def item(id):
    if id is None:
        items = get_items()
        if items:
            click.echo("Available items:")
            print_items(items)
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
        rich.print(f"\n[green]Collection with ID {id} was succesfully removed[/green]\n")
    except ValueError as e:
        click.echo(str(e))


if __name__ == "__main__":
    cli()
