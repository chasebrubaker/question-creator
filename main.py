import json
import os
import time
import sys
import platform
from pathlib import Path
from rich.console import Console
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.logging import RichHandler
from rich.prompt import Prompt, Confirm
import logging

APP_NAME = "Question Creator"
VERSION = "1.0.0"

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

def save_question(question_data, filename='questions.json'):
    data_file = get_document_path() / filename
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
                save_question(question_data)
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
        
if __name__ == "__main__":
    main()