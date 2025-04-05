from pymongo import MongoClient

client = MongoClient("mongodb+srv://marcosrequenagut:Markitos2001@master.dxuf4.mongodb.net/")
db = client["laboratory"]
collection = db["animals"]

# Define the filter to label the animals
create_labels = [
    ({"walks_on_n_legs": 2, "has_wings": True}, "chicken"),
    ({"walks_on_n_legs": 2, "has_wings": False}, "kangaroo"),
    ({"walks_on_n_legs": 4, "weight": {"$gte": 100}}, "elephant"),
    ({"walks_on_n_legs": 4, "weight": {"$lt": 100}}, "dog"),
]


for condition, label in create_labels:
    # Update the documents that match the filter
    result = collection.update_many(condition, {"$set": {"label": label}})
    print(f"Labeled {result.modified_count} as '{label}'")

# If we sum all the labels, we will find that 490 animals are labeled, but 10 are not, because we have 500 rows.
# This might indicate some errors in the database. Let's investigate.

# Let's analize the animals with an unusual number of legs, which is likely a data error.
query = {"walks_on_n_legs": {"$nin": [2, 4]}}
result = collection.find(query)

for doc in result:
    print(doc)

# Delete those wrong rows from the database
delete_result = collection.delete_many(query)
print(f"\nDeleted {delete_result.deleted_count} documents with unusual number of legs.")

# Show the number of documents in the collection after deletion and the number of documents with each label
total_count = collection.count_documents({})
print(f"\nTotal documents in the collection: {total_count}")

# Count the number of dogs
dog_count = collection.count_documents({"label": "dog"})
print(f"Total dogs: {dog_count}")

# Count the number of chickens
chicken_count = collection.count_documents({"label": "chicken"})
print(f"Total chickens: {chicken_count}")

# Count the number of kangaroos
kangaroo_count = collection.count_documents({"label": "kangaroo"})
print(f"Total kangaroo: {kangaroo_count}")

# Count the number of elephants
elephant_count = collection.count_documents({"label": "elephant"})
print(f"Total elephant: {elephant_count}")

print(f"\nTotal labeled animals: {dog_count + chicken_count + kangaroo_count + elephant_count}")

if total_count == (dog_count + chicken_count + kangaroo_count + elephant_count):
    print("All animals are labeled correctly.")
else:
    print("There are some animals that are not labeled correctly.")
    