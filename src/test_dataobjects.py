import unittest
import sqlite3
from dataobjects import Collection, Item, Connection


class TestItem(unittest.TestCase):

    def test_item_creation(self):
        item = Item(1, "Tent", 2500.0, "Lightweight tent", "Shelter")
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, "Tent")
        self.assertEqual(item.weight, 2500.0)
        self.assertEqual(item.note, "Lightweight tent")
        self.assertEqual(item.category, "Shelter")
        self.assertEqual(str(item), "1: Tent, 2500.0")


class TestCollection(unittest.TestCase):
    items = {
        "Shelter": [Item(1, "Tent", 2500.0, "Lightweight tent", "Shelter")],
        "Sleep": [Item(2, "Sleeping Bag", 1500.0, "Warm sleeping bag", "Sleep")]
    }

    collection = Collection(1, "Camping Gear", "Essential camping items", items)

    def test_collection_creation(self):
        collection = Collection(5, "Kungsleden", "Swedens King Trail", {})
        self.assertEqual(collection.id, 5)
        self.assertEqual(collection.name, "Kungsleden")
        self.assertEqual(collection.description, "Swedens King Trail")

    def test_get_category_weights(self):
        expected_weights = {
            "Shelter": 2500.0,
            "Sleep": 1500.0
        }
        self.assertEqual(self.collection.get_category_weights(), expected_weights)

    def test_get_total_weight(self):
        collection = Collection(1, "Camping Gear", "Essential camping items", self.items)
        expected_total_weight = 4000.0
        self.assertEqual(collection.get_total_weight(), expected_total_weight)


class TestConnection(unittest.TestCase):

    def test_connection_creation(self):
        conn = Connection(":memory:")  # Using an in-memory database for testing
        self.assertIsNotNone(conn.connection)
        self.assertIsNotNone(conn.cursor)
        conn.close()

    def test_commit_and_close(self):
        conn = Connection(":memory:")
        conn.commit()  # Should not raise any exceptions
        conn.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            conn.cursor.execute("SELECT 1")  # Should raise an error since the connection is closed


if __name__ == '__main__':
    unittest.main()
