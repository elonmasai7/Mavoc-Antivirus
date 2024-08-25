import os
import ctypes
import platform
import psutil
import time

def is_debugger_present():
    """Check if the process is being debugged."""
    return ctypes.windll.kernel32.IsDebuggerPresent()

def check_sandbox_files():
    """Check for files often present in sandbox environments."""
    sandbox_files = [
        r"C:\windows\system32\drivers\VBoxMouse.sys",  # VirtualBox
        r"C:\windows\system32\drivers\vmmouse.sys",    # VMware
        r"C:\windows\system32\drivers\vmhgfs.sys",     # VMware
    ]
    for file in sandbox_files:
        if os.path.exists(file):
            return True
    return False

def check_running_processes():
    """Check for processes commonly found in sandboxes."""
    sandbox_processes = ["VBoxService.exe", "vmtoolsd.exe", "vboxtray.exe"]
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in sandbox_processes:
            return True
    return False

def check_system_metrics():
    """Check system metrics like CPU cores and memory to detect virtual environments."""
    if psutil.virtual_memory().total < 2 * 1024 * 1024 * 1024:  # Less than 2GB RAM
        return True
    if psutil.cpu_count() <= 2:  
        return True
    return False

def check_timing():
    """Check for timing discrepancies that might indicate a virtualized environment."""
    start_time = time.time()
    time.sleep(1)
    elapsed_time = time.time() - start_time
    if elapsed_time > 1.1:  # Significantly more than 1 second
        return True
    return False

def main():
    if is_debugger_present():
        print("Debugger detected!")
    elif check_sandbox_files():
        print("Sandbox files detected!")
    elif check_running_processes():
        print("Sandbox-related processes detected!")
    elif check_system_metrics():
        print("System metrics indicative of a virtual environment!")
    elif check_timing():
        print("Timing discrepancies detected!")
    else:
        print("No sandbox detected.")

if __name__ == "__main__":
    main()
