CREATE TABLE "collection_items" (
	"collection_id"	INTEGER,
	"item_id"	INTEGER,
	FOREIGN KEY("collection_id") REFERENCES "collection"("collectionID"),
	FOREIGN KEY("item_id") REFERENCES "item"("itemID"),
	PRIMARY KEY("collection_id","item_id")
)
CREATE TABLE "collection"
(
    collectionID INTEGER
        primary key autoincrement,
    description  TEXT,
    name         TEXT not null
)

CREATE TABLE "item" (
	"itemID"	INTEGER,
	"name"	TEXT,
	"weight"	INTEGER,
	"note"	TEXT,
	"category"	TEXT,
	PRIMARY KEY("itemID" AUTOINCREMENT)
)
