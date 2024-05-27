import os
import re
import numpy as np

def rename_files(directory, starting_value):
    # Get list of files in the directory
    files = os.listdir(directory)

    # Initialize counter
    count = 1
    numbers = []
    dirs = []
    filenames = []
    new_names = []
    for filename in files:
        # Check if the file is a regular file
        if os.path.isfile(os.path.join(directory, filename)):
            # Get the file extension
            _, extension = os.path.splitext(filename)
            if extension in [".json", ".png"]:
                number = re.findall(r'\d+', filename)
                nam = filename.split("_")
                nam = nam[0]
                number = int(number[-1])
                numbers.append(number)
                dirs.append(directory)
                filenames.append(filename)
                new_name = f"{nam}_{number+starting_value}{extension}"
                new_names.append(new_name)
                count+=1
    
    # 
    numbersp = np.array(numbers) 
    sort_inds = np.argsort(numbersp)
    sort_inds = sort_inds[::-1]
    
    for i in sort_inds:
        # Rename the file
        print(new_names[i])
        os.rename(os.path.join(dirs[i], filenames[i]), os.path.join(dirs[i], new_names[i]))

if __name__ == "__main__":
    directory = "./slides"
    starting_value = 20
    
    rename_files(directory, starting_value)
    print("Files renamed successfully.")
