import sqlite3


def initialize_database(db_path: str):
    # SQL statements to create the tables
    sql_statements = """
    CREATE TABLE "collection_items" (
        "collection_id" INTEGER,
        "item_id" INTEGER,
        FOREIGN KEY("collection_id") REFERENCES "collection"("id"),
        FOREIGN KEY("item_id") REFERENCES "item"("id"),
        PRIMARY KEY("collection_id", "item_id")
    );

    CREATE TABLE "collections" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "description" TEXT,
        "name" TEXT NOT NULL
    );

    CREATE TABLE "items" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT,
        "weight" INTEGER,
        "note" TEXT,
        "category" TEXT
    );
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript(sql_statements)

    conn.commit()
    conn.close()
