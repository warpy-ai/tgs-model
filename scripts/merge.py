import json


def format_to_merge_json():

    with open("data/new-nl2bash-data.json", "r") as f:
        data1 = json.loads(f.read())

    with open("data/nl2bash-data.json", "r") as f:
        data2 = json.loads(f.read())

    formatted_data_1 = {}
    for key, value in data1.items():
        if isinstance(value, str):
            try:
                parsed_value = json.loads(value)
                formatted_data_1[key] = parsed_value
            except:
                print("error")
                formatted_data_1[key] = value

    last_key = max(int(k) for k in data2.keys())

    increment_data1 = {str(last_key + 1 + i): value for i, (key, value) in enumerate(
        sorted(formatted_data_1.items(), key=lambda item: int(item[0])))}

    last_key += len(increment_data1)

    merged_data = {**data2, **increment_data1}

    return merged_data


merged = format_to_merge_json()

with open("data/merged-nl2bash-data.json", "w") as f:
    json.dump(merged, f, indent=4)

print("Finished")
