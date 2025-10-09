import json
import os
import time
import sys
from rich.console import Console
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.logging import RichHandler
from rich.prompt import Prompt, Confirm
import logging


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_bar(duration: int, console: Console, loading_text: str = "loading..."):
    # for i in range(length + 1):
    #     percent = int((i / length) * 100)
    #     bar = "#" * i + "-" * (length - i)
    #     sys.stdout.write(f"\r[{bar}] {percent}%")
    #     sys.stdout.flush()
    #     time.sleep(duration / length)
    # print()  # move to the next line\
    
    # with Progress(
    #     SpinnerColumn(),
    #     TextColumn("[progress.description]{task.description}"),
    # ) as progress:
    #     task = progress.add_task(loading_text, total=None)
    #     time.sleep(duration)  # simulate installing
    #     progress.remove_task(task)
    
    with console.status(f"[bold green]{loading_text}", spinner="dots"):
        time.sleep(duration)
    
def create_question():
    question = Prompt.ask("Enter your question")
    answer = Prompt.ask("Enter the answer")
    return {"question": question, "answer": answer}

def save_question(question_data, filename='questions.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"questions": []}
    question_data["id"] = len(data["questions"]) + 1
    data["questions"].append(question_data)
    with open(filename, 'w') as file:
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
        running = False
        loading_bar(2, console, "Exiting...")
        
        print ("Goodbye!👋")
        time.sleep(2)
        
if __name__ == "__main__":
    main()