class Collection:
    def __init__(
        self,
        collection_id: int,
        name: str,
        description: str,
        items,
    ):
        self.collection_id = collection_id
        self.name = name
        self.description = description
        self.items = items


class Item:
    def __init__(
        self,
        item_id: int,
        name: str,
        weight: float,
        note: str,
        category: str,
    ):
        self.id = item_id
        self.name = name
        self.weight = weight
        self.note = note
        self.category = category
