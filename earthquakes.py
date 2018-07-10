import requests #pip3 install requests
import json
from datetime import datetime


url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
response = requests.get(url)

geodata = json.loads(response.content)

result = []
for record in geodata["features"]:
    props = record["properties"]
    place = props["place"]
    if "California" in place:
        magnitude = props["mag"]
        timestamp = props["time"]
        date = datetime.utcfromtimestamp(timestamp % 1000)
        result.append(date.isoformat() + " | " + place + " | Magnitude: " + str(magnitude))

result.sort()

print("\n".join(result))