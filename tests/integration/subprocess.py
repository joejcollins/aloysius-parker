"""Run a subprocess."""
import subprocess
import time
from typing import Generator


def run_subprocess(command: list) -> Generator:
    """Run the command and yield once the process is running."""
    server_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,  # capture stdout of the subprocess
        stderr=subprocess.PIPE,  # capture stderr of the subprocess
        text=True,
        bufsize=1,
    )
    time.sleep(3)  # Pause for the server to start
    yield
    server_process.terminate()
    server_process.wait()
    print(server_process.stdout.read())
    print(server_process.stderr.read())
