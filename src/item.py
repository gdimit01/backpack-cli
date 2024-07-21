from typing import List

import rich

from dataobjects import Item


def print_items(items: List[Item]):
    for item in items:
        rich.print(f"[dim]{item.id}[/dim] [bold]{item.name}[/bold]")
