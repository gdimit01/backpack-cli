import click
from rich import print
from database import (
    get_all_items,
    get_collections,
    create_new_item,
    create_collection,
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


@view.command()
def collection():
    print("viewing collection")


@view.command()
def item():
    print("viewing item")


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
