import subprocess
import os
import shutil

def check_dependencies():
    missing = []
    if not shutil.which("smbclient"):
        missing.append("smbclient")
    return missing

def print_via_smbclient(original_file_path, username, password, printer_name):
    # Command: smbclient -U nusstu/[username] //nts27.comp.nus.edu.sg/[printer_name] -c "print [file path]"
    
    # Wrap the original_file_path with quotes inside the "print ..." command
    print_cmd = 'print "{}"'.format(original_file_path)
    
    cmd = [
        "smbclient", 
        "-U", "nusstu/{}".format(username), 
        "//nts27.comp.nus.edu.sg/{}".format(printer_name), 
        "-c", print_cmd
    ]
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Provide password to stdin
    stdout, stderr = process.communicate(input=password + "\n")
    
    return stdout, stderr, process.returncode

def execute_printing(original_file_path, username, password, printer_name, duplex=True):
    if not os.path.exists(original_file_path):
        return f"File not found: {original_file_path}", False

    try:
        # Note: duplex setting is currently ignored as it was handled by enscript.
        # smbclient 'print' command sends the raw file to the printer queue.
        stdout, stderr, returncode = print_via_smbclient(original_file_path, username, password, printer_name)
        
        all_output = stdout + "\n" + stderr
        success = "putting file" in all_output
        
        return all_output, success
    except Exception as e:
        return str(e), False

