from typing import List, Dict
from dataobjects import Item
import rich


def print_items(items: List[Item]):
    for item in items:
        rich.print(f"[dim]{item.id}[/dim] [bold]{item.name}[/bold]")
