import click
from rich import print
from database import (
    get_all_items,
    get_collections,
    create_new_item,
    create_collection,
    get_item,
)


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
        print()
        click.echo("Items in the database:")
        print()
        for item in items:
            print(f"[dim]{item.id}:[/dim] {item.name} {item.weight} {item.category}")
        print()

    else:
        click.echo("No items found in the database.")


@list.command()
def collections():
    collections = get_collections()
    if collections:
        print()
        print("Collections in the database:")
        print()
        for collection in collections:
            print(f"[bold]{collection[0]}[/bold] [dim]{collection[1]}[/dim]")
        print()

    else:
        print("[red]No collections found in the database[/red]")


# Subcommands under 'add'
@add.command()
def item():
    create_new_item()


@add.command()
def collection():
    create_collection()


# Subcommands under 'view'
@view.command()
@click.argument("id", required=False, type=int)
def collection(id):
    if id is None:
        collections = get_collections()
        if collections:
            click.echo("Avaible collections:")
            for collection in collections:
                print(f"{collection.name}")
        else:
            click.echo("No collections found in the database")

        id = click.promt("Enter the ID of the collection you want to view", type=int)

    try:
        collection = get_collection(id)
        print(f"{collection.name}")
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

        id = click.prompt("Enter the ID of the item you want to view", type=int)

    try:
        item = get_item(id)
        print(
            f"Item ID: {item.id}, Name: {item.name}, Weight: {item.weight}, Category: {item.category}"
        )
    except ValueError as e:
        click.echo(str(e))


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
