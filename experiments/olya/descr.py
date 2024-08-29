# data <- json
import json
data = json.loads(room.json)
level = 1
descs = [desc for desc in data["room1"]["descriptions"] if desc["level"] <= level]
desc = " ".join(descs)
print(desc)