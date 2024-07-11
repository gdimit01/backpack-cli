import sqlite3


class Collection:
    def __init__(
        self,
        collection_id: int,
        name: str,
        description: str,
        items: map,
    ):
        self.id = collection_id
        self.name = name
        self.description = description
        self.items = items

        #  TODO: define methods to calculate weight and stats etc


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
        self.cursor = self.conn.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()
