import os
import sftp_download  # Import your first script
import backup_tool    # Import your second script

def run_full_workflow():
    print("--- Phase 1: Downloading from Server ---")
    try:
        # Calls the function from your sftp_download script
        sftp_download.download_sftp_project()
        
        print("\n--- Phase 2: Creating Local Backup and Cleaning ---")
        # Calls the function from your backup_tool script
        backup_tool.localized_backup()
        
        print("\n--- Workflow Complete ---")
        os.system('say "All tasks completed successfully."')
        
    except Exception as e:
        print(f"Workflow failed at some point: {e}")
        os.system('say "The automated workflow failed."')

if __name__ == "__main__":
    run_full_workflow()