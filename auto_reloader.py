import os
import sys
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    """Handles file system events and restarts the Flask server."""
    
    def on_any_event(self, event):
        # Ignore .pyc files and __pycache__ directories
        if event.is_directory or event.src_path.endswith('.pyc'):
            return
        print(f'Change detected: {event.src_path}')
        global flask_process
        if flask_process:
            # Terminate the existing Flask process
            flask_process.terminate()
            flask_process.wait()
        # Start a new Flask process
        flask_process = subprocess.Popen(flask_command, shell=True)

if __name__ == "__main__":
    path = '.'  # Directory to watch
    flask_command = 'flask run'  # Flask command to run
    flask_process = None

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        # Initially start the Flask app
        flask_process = subprocess.Popen(flask_command, shell=True)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    if flask_process:
        flask_process.terminate()
