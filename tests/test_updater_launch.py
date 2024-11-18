import os
import psutil
import signal
import sys

celer_sight_source = os.environ["CELER_SIGHT_AI_HOME"]
sys.path.append(celer_sight_source)
from updater import main


def terminate_processes_using_file(file_path):
    file_path = os.path.abspath(file_path)
    terminated_processes = []

    python_processes = [
        p
        for p in psutil.process_iter(["name", "open_files"])
        if p.info["name"] in ["python", "python.exe"]
    ]

    for process in python_processes:
        if any(open_file.path == file_path for open_file in process.info["open_files"]):
            try:
                process.send_signal(signal.SIGTERM)
                terminated_processes.append(process)
            except psutil.AccessDenied:
                print(f"Access denied when trying to terminate process {process.pid}")
            except psutil.NoSuchProcess:
                print(f"Process {process.pid} does not exist")

    return terminated_processes


file_path = "path/to/your/file"
terminated_processes = terminate_processes_using_file(file_path)

if terminated_processes:
    print(
        f"Terminated processes using file {file_path}: {', '.join(str(p.pid) for p in terminated_processes)}"
    )
else:
    print(f"No processes using file {file_path} were found or terminated")

p = os.path.dirname(os.path.abspath(__file__))
file_to_lunch = os.path.join(p, "test_files_runs.py")

# launch_update(file_to_lunch)
