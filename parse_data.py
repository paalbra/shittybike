import glob
import json
import re
import sys

filenames = sorted(filename for filename in glob.glob("./data/*.json"))

point_count = 0
station_sums = {}

if len(sys.argv) != 2 or sys.argv[1] not in ["info", "data"]:
    print(f"USAGE: {sys.argv[0]} (info|data)")
    sys.exit(1)

if sys.argv[1] == "info":
    for filename in filenames:
        with open(filename) as f:
            content = f.read()

        try:
            data = json.loads(content)
        except:
            print(f"{filename}: JSON ERROR")
            continue

        if "errors" in data:
            print(f"{filename}: data ERROR")
            continue

        point_count += 1

        docks = data["data"]["dockGroups"]

        total_docks = len(docks)
        total_vehicles = sum(dock["availabilityInfo"]["availableVehicles"] for dock in docks)
        avg_vehicles = total_vehicles/total_docks
        
        for dock in docks:
            station_sums[dock["title"]] = station_sums.get(dock["title"], 0) + dock["availabilityInfo"]["availableVehicles"]

        print(f"{filename}: {total_docks=} {total_vehicles=} {avg_vehicles=:.2f}")

    for station_name, station_sum in sorted(station_sums.items(), key=lambda e: e[1]):
        avg_vehicles = station_sum/point_count
        print(f"SUMMARY: {station_name=} {point_count=} {avg_vehicles=:.4f}")

if sys.argv[1] == "data":

    new_data = {}

    for index, filename in enumerate(filenames):
        match = re.match(r"./data/json_(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)\d\d.json", filename)
        year, month, day = match.group(1), match.group(2), match.group(3)
        hour, minute = match.group(4), match.group(5)
        timestamp = f"{year}-{month}-{day}T{hour}:{minute}"

        with open(filename) as f:
            content = f.read()

        try:
            data = json.loads(content)
        except:
            #print(f"{filename}: JSON ERROR")
            continue

        if "errors" in data:
            #print(f"{filename}: data ERROR")
            continue

        docks = data["data"]["dockGroups"]
        

        for dock in docks:
            if dock["id"] not in new_data:
                new_data[dock["id"]] = {
                    "id": dock["id"],
                    "name": dock["name"],
                    "title": dock["title"],
                    "state": dock["state"],
                    "enabled": dock["enabled"],
                    "lat": dock["coord"]["lat"],
                    "lng": dock["coord"]["lng"],
                    "data": []
                }
            
            new_data[dock["id"]]["data"].append({
                "x": timestamp,
                "y": dock["availabilityInfo"]["availableVehicles"]
            })

    print(json.dumps(new_data))
