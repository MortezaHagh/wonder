import os
import json

def update_slide_names(directory):
    for filename in os.listdir(directory):
        if filename.startswith("zone_") and filename.endswith(".json"):
            # Extracting the number from the filename
            number = filename.split('_')[1].split('.')[0]
            with open(os.path.join(directory, filename), 'r+') as file:
                data = json.load(file)
                # Updating the slide_name field
                data['slide_name'] = f"slide_{number}"
                # Rewind the file pointer to the beginning before writing
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

# Update the directory path with your directory containing the JSON files
directory_path = './zones'
update_slide_names(directory_path)
