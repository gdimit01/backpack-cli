import click
from rich import print
from database import (
    get_all_items,
    get_collections,
    create_new_item,
    create_collection,
    get_item,
    get_collection,
    add_items_to_collection,
    delete_item,
    delete_collection,
)
import sys


# Click command group
@click.group()
def cli():
    pass


# Group for list commands
@cli.group()
def list():
    """List items, collections, etc."""
    pass


@cli.group()
def view():
    """View items, collections, etc."""
    pass


# Group for add commands
@cli.group()
def add():
    """Add items, collections, etc."""
    pass



# Subcommands under 'list'
@list.command()
def items():
    items = get_all_items()
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
            print(f"[dim]{collection.id}:[/dim] [bold]{collection.name}[/bold] [italic]{collection.description}[/italic]")
        print()

    else:
        print("\n[red]No collections found in the database[/red]\n")


# Subcommands under 'add'
@add.command()
def item():
    create_new_item()


@add.command()
def collection():
    create_collection()

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
        print(f"{collection.name}")
        print(collection.items)
    except ValueError as e:
        click.echo(str(e))


@view.command()
@click.argument("id", required=False, type=int)
def item(id):
    if id is None:
        items = get_all_items()
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
        items = get_all_items()
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
