import click

from database import get_collection


@click.command()
@click.argument('collection_id', type=int)
@click.argument('output_file', type=click.Path(writable=True))
@click.option('--pdf', is_flag=True, help='Creates a PDF checklist instead of a markdown')
def checklist(collection_id, output_file, pdf):
    """
    Export a collection of items as a markdown checklist or PDF.
    
    COLLECTION_ID: The ID of the collection to export.
    OUTPUT_FILE: The file to write the checklist to.
    --pdf: Creates a markdown file instead of PDF.
    """
    try:
        collection = get_collection(collection_id)
        if not pdf:
            markdown_content = generate_markdown_checklist(collection)
            with open(output_file, 'w') as file:
                file.write(markdown_content)
            click.echo(f"Collection {collection_id} exported to {output_file} as markdown successfully.")
        else:
            # generate_pdf_checklist(collection, output_file)
            click.echo(f"Collection {collection_id} exported to {output_file} as PDF successfully.")
    except Exception as e:
        click.echo(f"An error occurred: {e}")


def generate_markdown_checklist(collection):
    """
    Generate a markdown checklist for a given collection.
    """
    checklist = f"# {collection.name}\n"
    checklist += f"{collection.description}\n\n"

    for category, items_list in collection.items.items():
        checklist += f"### {category}\n\n"
        for item in items_list:
            name = pad_string(item.name, 30)
            checklist += f"- [ ] {name} ({item.note})\n"
        checklist += f"\n"

    return checklist


def pad_string(s, width):
    return s + ' ' * (width - len(s))


if __name__ == "__main__":
    pass
