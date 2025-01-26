import json

def create_name_timestamp(data: str) -> None:
    """
    Given a predefined structure of AI generated data, create a JSON file
    consisting of a list of dictionaries that track the following data...
    1. Timestamp
    2. First Name
    3. Last Name
    4. Category (type of play)
    """
    structured_data = []
    previous_timestamp = None
    
    for line in data.strip().split("\n"):
        if "->" not in line:
            continue

        parts = line.split("->")
        # Extract timestamp, name, category
        timestamp = parts[0].strip("[]")
        first_name, last_name = parts[1].split()
        category = parts[2]

        if category != "None":
            minutes, seconds = map(int, timestamp.split(":"))
            total_seconds = minutes * 60 + seconds
            
            if previous_timestamp is None or total_seconds - previous_timestamp >= 5:
                structured_data.append({
                    "timestamp": timestamp,
                    "first_name": first_name,
                    "last_name": last_name,
                    "category": category
                })
                previous_timestamp = total_seconds

    with open("timestamps.json", "w") as file:
        json.dump(structured_data, file, indent=4)

