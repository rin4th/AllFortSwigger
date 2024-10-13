from rich.console import Console
from rich import print
from rich.panel import Panel
import os
import platform
import time

from core.utils import check_url
from parsers.html_parser import parse_lab_info

console = Console()
repeat = True
URL = ""
clear = "cls" if platform.system() == "Windows" else "clear"

def print_banner():
    print(r"""[bold blue]
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║    _    _ _   _____            _   ____          _                       ║
    ║   / \  | | | |  ___|__  _ __  | |_/ ___|_      _(_) __ _  __ _  ___ _ __ ║
    ║  / _ \ | | | | |_ / _ \| '__| | __\___ \ \ /\ / / |/ _` |/ _` |/ _ \ '__|║
    ║ / ___ \| | | |  _| (_) | |    | |_ ___) \ V  V /| | (_| | (_| |  __/ |   ║
    ║/_/   \_\_|_| |_|  \___/|_|     \__|____/ \_/\_/ |_|\__, |\__, |\___|_|   ║
    ║                                                    |___/ |___/           ║
    ╚══════════════════════════════════════════════════════════════════════════╝ [/bold blue]
    """)

if __name__ == "__main__":
    while repeat:
        print_banner()
        URL = console.input("[bold green]Enter the URL to attack: [/bold green]")
        html_content = check_url(URL)

        if html_content == None:
            print("[bold red]Invalid URL[/bold red]")
            break

        info_lab = parse_lab_info(URL)
        print()
        print(Panel(f"""[bold blue]Vulnerability Type: {info_lab[0]}\n \\
                    Lab Name: {info_lab[1]}\n \\
                    URL: {info_lab[2]}\n \\
                    Objective: {info_lab[3]}\n \\
                    Dificulty: {info_lab[4]}\n \\
                    [/bold blue]", title="Lab Information"""))
            


        

        repeat = input("\nDo you want to check another URL? (y/n): ").lower() == "y"

