import click
from fpdf import FPDF

# Import the function to retrieve a collection from the database
from database import get_collection

@click.command()
@click.argument('collection_id', type=int)
@click.argument('output_file', type=click.Path(writable=True))
@click.option('--pdf', is_flag=True, help='Creates a PDF checklist instead of a markdown file')
def checklist(collection_id, output_file, pdf):
    """
    Export a collection of items as a markdown checklist or PDF.
    
    COLLECTION_ID: The ID of the collection to export.
    OUTPUT_FILE: The file to write the checklist to.
    --pdf: Creates a PDF checklist instead of a markdown checklist.
    """
    try:
        collection = get_collection(collection_id)
        if not pdf:
            markdown_content = generate_markdown_checklist(collection)
            with open(output_file, 'w') as file:
                file.write(markdown_content)
            click.echo(f"Collection {collection_id} exported to {output_file} as markdown successfully.")
        else:
            # Generate PDF format checklist and save it to the specified file
            generate_pdf_checklist(collection, output_file)
            click.echo(f"Collection {collection_id} exported to {output_file} as PDF successfully.")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

def generate_markdown_checklist(collection):
    """
    Generate a markdown checklist for a given collection.
    """

    checklist = f"# {collection.name}\n{collection.description}\n\n"
    # Iterate over each category and its items in the collection
    for category, items_list in collection.items.items():
        checklist += f"### {category}\n\n"
        # Add each item in the category to the markdown list with a checkbox
        for item in items_list:
            name = pad_string(item.name, 30)
            checklist += f"- [ ] {name} ({item.note})\n"
        checklist += "\n"
    return checklist

def pad_string(s, width):
    """
    Pad a string with spaces to a specified width.
    Useful for aligning text in markdown or other text outputs.
    """
    return s + ' ' * (width - len(s))

def generate_pdf_checklist(collection, output_file):
    """
    Generate a PDF formatted checklist for a given collection.
    Outputs the PDF to the specified file.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', size=12)
    #pdf.set_font("Arial", size=12)
    # Add the collection name and description at the top of the PDF page
    pdf.set_font('DejaVu', size=18)
    pdf.cell(200, 10, txt=f"{collection.name}", ln=1)

    pdf.set_font('DejaVu', size=12)
    pdf.cell(200, 10, txt=f"{collection.description}", ln=1)

    # Iterate through each category and its items in the collection
    for category, items_list in collection.items.items():
        pdf.cell(200, 10, txt=f"{category}", ln=1)
        for item in items_list:
            pdf.cell(200, 10, txt=f" ☐ {item.name} ({item.note})", ln=1)

    # Save the generated PDF to the specified file
    pdf.output(output_file)

if __name__ == "__main__":
    # Execute the command line interface setup by the click library
    checklist()
