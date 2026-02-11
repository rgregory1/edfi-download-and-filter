import os
import paramiko
import stat
from pathlib import Path
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

def sftp_get_recursive(sftp, remote_dir, local_dir):
    """
    Recursively downloads files and folders from a remote SFTP server.
    """
    # Create the local directory if it doesn't exist
    local_dir.mkdir(parents=True, exist_ok=True)
    
    # Look at everything inside the current remote folder
    for entry in sftp.listdir_attr(remote_dir):
        remote_path = f"{remote_dir}/{entry.filename}"
        local_path = local_dir / entry.filename
        
        # Check if the entry is a directory
        if stat.S_ISDIR(entry.st_mode):
            # It's a folder! Go deeper (recursion)
            print(f"Entering directory: {entry.filename}")
            sftp_get_recursive(sftp, remote_path, local_path)
        else:
            # It's a file! Download it
            print(f"Downloading file: {entry.filename}")
            sftp.get(remote_path, str(local_path))

def download_sftp_project():
    # Credentials from .env
    host = os.getenv("SFTP_HOST")
    user = os.getenv("SFTP_USER")
    password = os.getenv("SFTP_PASS")

    # Define the remote and local paths
    remote_root = "/SLDS VR/SU021/From AOE/Ed-Fi/2026"
    local_root = Path(__file__).parent / "2026"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Connecting to {host}...")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Add this to force the client to load existing system keys
        ssh.load_system_host_keys()
        ssh.connect(host, username=user, password=password)
        sftp = ssh.open_sftp()

        print(f"Starting recursive download from {remote_root}...")
        sftp_get_recursive(sftp, remote_root, local_root)

        print("\nSuccess! Full directory structure downloaded.")
        os.system('say "Recursive download complete"')

    except Exception as e:
        print(f"Error: {e}")
        os.system('say "An error occurred with the server connection"')
    finally:
        ssh.close()

if __name__ == "__main__":
    download_sftp_project()