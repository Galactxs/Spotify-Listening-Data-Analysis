import json
import os
import glob

# ---  This script removes the ip address for each song play and placed the cleaned JSON files into the processed folder ---------

# navigate files 
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)

# build paths to data folders
RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

def remove_ip_and_save():
    # get sorted list of all of the streaming history files
    files = sorted(glob.glob(os.path.join(RAW_DIR, 'Streaming_History_Audio_*.json')))

    for filepath in files:
        # open and load JSON file
        with open(filepath, "r", encoding='utf-8') as f:
            data = json.load(f)

        # Remove ip_addr from each song play [for security reasons :)]
        cleaned = []
        for entry in data:
            new_entry = {}
            for k, v in entry.items():
                if k != 'ip_addr':
                    new_entry[k] = v
            cleaned.append(new_entry)
        
        # Get just filename from the full path
        filename = os.path.basename(filepath)
        # Build the output path in the processed folder
        out_path = os.path.join(PROCESSED_DIR, filename)

        # Save the cleaned data into the processed folder
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned, f, indent=2, ensure_ascii=False)

        print(f"{filename}: {len(cleaned)} entries saved")

# Only run if this file is exicuted directly
if __name__ == '__main__':
    remove_ip_and_save()
    
