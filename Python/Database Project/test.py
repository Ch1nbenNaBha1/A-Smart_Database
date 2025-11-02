import json

data = []
for i in range(1, 301):
    record = {
        "id": f"record_{i}",
        "data": {
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "score": (i * 7) % 100  # some pseudo-random score
        }
    }
    data.append(record)

with open("test_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("test_data.json created with 300 records!")
