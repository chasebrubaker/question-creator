import json
import os
import time
import sys
import shutil
import requests
import tempfile
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich import print
from rich.logging import RichHandler
from rich.prompt import Prompt, Confirm
import logging

APP_NAME = "Question Creator"
VERSION = "1.0.0"
REPO = "chasebrubaker/create-questions"

def get_platform_name() -> str:
    system = platform.system().lower()
    if system == 'windows':
        return 'windows.exe'
    elif system == 'darwin':  # macOS
        return "macos "
    else:  # Linux and other OS
        return "linux"

def get_latest_version() -> str:
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()["tag_name"].lstrip("v")

def download_binary(version, console: Console):
    platform_name = get_platform_name()
    url = f"https://github.com/{REPO}/releases/download/v{version}/{APP_NAME}-{platform_name}"
    tmp_path = os.path.join(tempfile.gettempdir(), f"{APP_NAME}-{platform_name}")
    with console.status(f"[bold green]Downloading {url}", spinner="dots"):
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    os.chmod(tmp_path, 0o755)
    return tmp_path

def replace_and_restart(new_binary_path):
    current_binary = sys.argv[0]
    helper_script = os.path.join(tempfile.gettempdir(), "update_helper.py")
    
    with open(helper_script, "w") as f:
        f.write(f"""
import os, sys, time, shutil, subprocess
time.sleep(1)
os.remove(r"{current_binary}")
shutil.move(r"{new_binary_path}", r"{current_binary}")
subprocess.Popen([r"{current_binary}"])
""")
        subprocess.Popen([sys.executable, helper_script])
        print("Updating...")
        sys.exit(0)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def loading_bar(duration: int, console: Console, loading_text: str = "loading..."):    
    with console.status(f"[bold green]{loading_text}", spinner="dots"):
        time.sleep(duration)
    
def create_question():
    question = Prompt.ask("Enter your question")
    answer = Prompt.ask("Enter the answer")
    return {"question": question, "answer": answer}

def get_document_path() -> Path:
    system = platform.system().lower()
    if system == 'windows':
        base = Path(os.environ.get("USERPROFILE", "")) / "Documents"
    elif system == 'darwin':  # macOS
        base = Path.home() / "Documents"
    else:  # Linux and other OS
        base = Path.home() / "Documents"
    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_document_path() -> Path:
    system = platform.system().lower()
    if system == 'windows':
        base = Path(os.environ.get("USERPROFILE", "")) / "Documents"
    elif system == 'darwin':  # macOS
        base = Path.home() / "Documents"
    else:  # Linux and other OS
        base = Path.home() / "Documents"
    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path

def save_question(question_data, console: Console, filename='questions.json', ) -> None:
    data_file = get_document_path() / filename
    data_file = get_document_path() / filename
    with console.status(f"[bold green]Saving question to {data_file}", spinner="dots") :
        try:
            with open(data_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"questions": []}
        question_data["id"] = len(data["questions"]) + 1
        data["questions"].append(question_data)
        with open(data_file, 'w') as file:
            json.dump(data, file, indent=4)
      


def main():
    console = Console()
    logging.basicConfig(level="INFO", handlers=[RichHandler()])
    log= logging.getLogger("rich")
    running = True
    try:
        console.clear()
        log.info(f"Starting {APP_NAME} v{VERSION}")
        time.sleep(1)
        console.clear()
        console.rule("[bold green] Welcome to the Question Creator!👋")
        print("To [bold red] exit [/ bold red], press Ctrl+C\n")
        while running:
            question_data = create_question()
            confirmation = Prompt.ask(
                    f"Question Data: {question_data} is this correct?  ",
                    choices=['y', 'n', ],
                    default='y'
                ).strip().lower()
            if confirmation == 'y' :
                save_question(question_data, console=console)
                loading_bar(3, console, "Saving question...")
                console.clear()
                log.info("Question saved successfully!")
                time.sleep(2)
                console.clear()
               
                
            else:
                print("Let's try again.")  
            
    except KeyboardInterrupt:
        console.clear()
        running = False
        loading_bar(2, console, "Exiting...")
        
        print ("Goodbye!👋")
        time.sleep(2)
        console.clear()
        sys.exit(0)
        
if __name__ == "__main__":
    main()