import subprocess
import os
import shutil

DEFAULT_DOMAIN = "nusstu"
PRINT_SERVER = "nts27b.res.nus.edu.sg"

def check_dependencies():
    missing = []
    if not shutil.which("smbclient"):
        missing.append("smbclient")
    return missing

def _normalise_account(username):
    username = username.strip()
    domain = DEFAULT_DOMAIN

    if "\\" in username:
        domain, username = username.split("\\", 1)
    elif "/" in username:
        domain, username = username.split("/", 1)

    return domain.lower(), username.strip().upper()

def _quote_smbclient_arg(value):
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'

def _build_smbclient_command(server, domain, username, original_file_path, printer_name):
    print_cmd = f"print {_quote_smbclient_arg(original_file_path)}"

    return [
        "smbclient",
        "-s", "/dev/null",
        "--option=client min protocol=SMB2",
        "--option=client max protocol=SMB3",
        "-U", f"{domain}/{username}",
        f"//{server}/{printer_name}",
        "-c", print_cmd,
    ]

def _format_debug_command(cmd):
    return "Command: " + " ".join(cmd)

def _run_smbclient(cmd, password):
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        stdout, stderr = process.communicate(input=password + "\n", timeout=60)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        stderr = stderr + "\nsmbclient timed out after 60 seconds."
    return stdout, stderr, process.returncode

def print_via_smbclient(original_file_path, username, password, printer_name):
    domain, normalised_username = _normalise_account(username)
    attempts = []

    cmd = _build_smbclient_command(
        PRINT_SERVER,
        domain,
        normalised_username,
        original_file_path,
        printer_name,
    )
    stdout, stderr, returncode = _run_smbclient(cmd, password)
    attempts.append((_format_debug_command(cmd), stdout, stderr, returncode))

    return stdout, stderr, returncode, attempts

def execute_printing(original_file_path, username, password, printer_name, duplex=True):
    if not os.path.exists(original_file_path):
        return f"File not found: {original_file_path}", False

    try:
        # Note: duplex setting is currently ignored as it was handled by enscript.
        # smbclient 'print' command sends the raw file to the printer queue.
        result = print_via_smbclient(original_file_path, username, password, printer_name)
        if len(result) == 4:
            stdout, stderr, returncode, attempts = result
        else:
            stdout, stderr, returncode = result
            attempts = []
        
        all_output = stdout + "\n" + stderr
        success = returncode == 0 and "NT_STATUS" not in all_output
        if not success and attempts:
            tried = "\n\nTried:\n" + "\n".join(item[0] for item in attempts)
            all_output = all_output + tried
        
        return all_output, success
    except Exception as e:
        return str(e), False
