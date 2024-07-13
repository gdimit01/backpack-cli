import sqlite3
from typing import Dict, List


class Collection:
    def __init__(
            self,
            id,
            name,
            desc,
            items
    ):
        self.id = id
        self.name = name
        self.description = desc
        self.items = items

    def get_category_weights(self) -> Dict[str, float]:
        weights = {}
        for category, item_list in self.items.items():
            total_weight = sum(item.weight for item in item_list)
            weights[category] = total_weight
        return weights


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


class Connection:
    def __init__(self, database: str):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def commit(self):
        self.connection.commit()
