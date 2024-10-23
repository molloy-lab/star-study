import os
import zipfile
import re

# Path to your ZIP file and new directory
zip_file_path = 'startle_simulations.zip'
output_directory = 'sashittal2023startle_used_in_startle'

# Regular expression to extract parameters from the filename
pattern1 = re.compile(r"n(\d+)_m(\d+)_d([\d\.]+)_s(\d+)_p([\d\.]+)_character_matrix\.csv")
pattern2 = re.compile(r"n(\d+)_m(\d+)_d([\d\.]+)_s(\d+)_p([\d\.]+)_tree.newick")
pattern3 = re.compile(r"n(\d+)_m(\d+)_d([\d\.]+)_s(\d+)_p([\d\.]+)_mutation_prior\.csv")
pattern4 = re.compile(r"n(\d+)_m(\d+)_d([\d\.]+)_s(\d+)_p([\d\.]+)_counts\.csv")
pattern5 = re.compile(r"n(\d+)_m(\d+)_d([\d\.]+)_s(\d+)_p([\d\.]+)_edge_labels\.csv")
pattern6 = re.compile(r"n(\d+)_m(\d+)_d([\d\.]+)_s(\d+)_p([\d\.]+)_edgelist\.csv")

patterns = [pattern1,pattern2,pattern3,pattern4,pattern5,pattern6]

# Open the ZIP file
for pattern in patterns:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Iterate through each file in the ZIP archive
        print(zip_ref.namelist())
    
        for file_name in zip_ref.namelist():
            # Match the pattern to extract parameters
            match = pattern.match(file_name)
            if match:
            # Extract parameters
                cells, characters, dropout, seed, mutationrate = match.groups()

                if float(mutationrate) != 0.1 or float(dropout) != 0.15:
                    continue

                # Create a new directory structure based on the parameters
                new_dir = os.path.join(output_directory, f"cells_{cells}_characters_{characters}_dropout_{dropout}_mutationrate_{mutationrate}",str(seed))
                
                if not os.path.isdir(new_dir):
                    os.makedirs(new_dir, exist_ok=True)

            # Define the new file path
                new_file_path = os.path.join(new_dir, os.path.basename(file_name))

            # Extract and write the file to the new directory
                with zip_ref.open(file_name) as source_file, open(new_file_path, 'wb') as target_file:
                    target_file.write(source_file.read())
