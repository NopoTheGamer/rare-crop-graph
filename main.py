import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

with open("config.json", 'r', encoding="UTF-8") as file:
    data = json.load(file)

data = data["rareCrop"]

times = [
    (1777784100000, 1777821300000), # Sugar Cane, Cocoa Beans, Moonflower
    (1777821300000, 1777858500000), # Carrot, Potato, Wart
    (1777858500000, 1777895700000), # Cactus, Mushroom, Sunflower
    (1777895700000, 1777932900000), # Sugar Cane, Moonflower, Cocoa Beans
    (1777932900000, 1777970100000), # Wheat, Pumpkin, Melon
    (1777970100000, 1778007300000), # Carrot, Mushroom, Sunflower
    (1778007300000, 1778044500000), # Wart, Sugar Cane, Cocoa Beans
    (1778044500000, 1778044500000), # Potato, Wildrose, Moonflower
]

# do "del data["dropTimes"]["Drop Name"]" to hide that drop from the graph
# del data["dropTimes"]["Warty"]
# del data["dropTimes"]["Fermento"]
# del data["dropTimes"]["Helianthus"]
# del data["dropTimes"]["Seasoning"]
# del data["dropTimes"]["Epic Slug"]
del data["dropTimes"]["Ethereal Vine"]


# set this to show just a specific section of the event
# set to -1 to show all the data
# i.e. set to 1 for only the Carrot Potato Wart data
currentCrop = -1

rows = []
for category, timestamps in data["dropTimes"].items():
    for ts in timestamps:
        if currentCrop >= 0:
            if times[currentCrop][0] > ts:
                continue
            if times[currentCrop][1] < ts:
                continue
        rows.append({
            "category": category,
            "time": datetime.fromtimestamp(ts/1000)
        })

df = pd.DataFrame(rows)

df = df.sort_values("time")

df["time_bin"] = df["time"].dt.floor("min")

grouped = df.groupby(["time_bin", "category"]).size().unstack(fill_value=0)

cumulative = grouped.cumsum()

cumulative.plot(figsize=(10,6))

plt.title("Cumulative Drops Over Time")
plt.xlabel("Time")
plt.ylabel("Total Drops")
plt.legend(title="Category")
plt.tight_layout()
plt.show()