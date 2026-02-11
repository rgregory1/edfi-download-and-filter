import shutil
import os
import subprocess # Best for opening Finder windows
from pathlib import Path
from datetime import datetime

def localized_backup():
    # 'base_path' is the folder where THIS script is currently sitting
    base_path = Path(__file__).parent
    
    # Define paths relative to the script location
    source_folder = base_path / "2026" / "checks"
    exclusions_file = base_path / "exclusions.txt"
    
    # Create the timestamped name
    date_stamp = datetime.now().strftime("%Y-%m-%d")
    destination_folder = base_path / f"checks_copy_{date_stamp}"

    try:
        # 1. Verify source exists
        if not source_folder.exists():
            print(f"Error: Could not find {source_folder}")
            os.system('say "Source folder missing"')
            return

        # 2. Perform the copy
        shutil.copytree(source_folder, destination_folder)
        
        # 3. Handle Exclusions
        if exclusions_file.exists():
            with open(exclusions_file, "r") as f:
                to_remove = [line.strip() for line in f if line.strip()]
            
            for filename in to_remove:
                file_path = destination_folder / filename
                if file_path.exists():
                    file_path.unlink()
                    print(f"Removed: {filename}")
        
        # 4. Success!
        print(f"Done! Created: {destination_folder.name}")
        
        # Speak the confirmation
        os.system('say "Check backup complete"')
        
        # Open the new folder in Finder
        subprocess.run(["open", str(destination_folder)])

    except FileExistsError:
        print("Error: Folder for today already exists.")
        os.system('say "Folder already exists"')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        os.system('say "An error occurred"')

if __name__ == "__main__":
    localized_backup()