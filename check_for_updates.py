# Author: Daethyra (Daemon Carino)

# This Python module provides functions to check for file updates 
#    ONLY to the files listed in the files_to_check list. (Ln, 44)

""" This module supports a streamlined self-update process for the Windows installation files. """

import subprocess
import logging

# Initialize and set logging level
logging.basicConfig(filename="script-update.log", level=logging.INFO, format='%(levelname)s: %(message)s')

def get_changed_files(files_to_check):
    """
    Fetches and identifies if files_to_check have changed between local and remote.

    Args:
        files_to_check (list): List of file names to check for updates.

    Returns:
        list: List of changed files or None if an error occurs.
    """
    try:
        # Fetch origin/main
        subprocess.run(["git", "fetch", "origin", "main"])
        
        # Get changed files
        changed_files = subprocess.getoutput("git diff HEAD..origin/main --name-only").split("\n")
        return [f for f in changed_files if f in files_to_check]
    
    except Exception as e:
        logging.error(f"Failed to get changed files: {e}")
        return None

def update_files(changed_files):
    """
    Updates the files passed in changed_files list.

    Args:
        changed_files (list): List of changed file names to update.
    """
    # Update files
    for file in changed_files:
        try:
            # Checkout the file from origin/main
            subprocess.run(["git", "checkout", "origin/main", "--", file])
            
            logging.info(f"Successfully updated {file}")
            
        except Exception as e:
            logging.error(f"Failed to update {file}: {e}")

# Run the script
if __name__ == "__main__":
    
    # List of files to check for updates
    files_to_check = ['start', 'update'] ### <--- Configure files to check HERE ---> ###
    logging.info(f"Files to check: {files_to_check}")
    
    # Get changed files
    changed_files = get_changed_files(files_to_check)
    logging.info(f"Changed files: {changed_files}")

    # Update files if changed_files is not None
    if changed_files is not None:
        update_files(changed_files)
    else:
        logging.info("No updates needed.")
