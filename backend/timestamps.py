import json

def create_name_timestamp(data: str) -> None:
    """
    Given a predefined structure of AI generated data, create a list of dictionaries that track the following data...
    1. Timestamp
    2. First Name
    3. Last Name
    """
    structured_data = []
    
    for line in data.strip().split("\n"):
        if "->" not in line:
            continue

        parts = line.split("->")
        # Extract timestamp, name, category
        timestamp = parts[0].strip("[]")
        first_name, last_name = parts[1].split()
            

        structured_data.append({
            "timestamp": timestamp,
            "first_name": first_name,
            "last_name": last_name
        })

    return structured_data

