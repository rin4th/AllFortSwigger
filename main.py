from rich.console import Console
from rich import print
from rich.panel import Panel
import os
import platform
import time

from ui.rich_components import print_banner
from core.utils import check_url
from parsers.html_parser import parse_lab_information

console = Console()
repeat = True
URL = ""
clear = "cls" if platform.system() == "Windows" else "clear"

while repeat:
    print_banner()
    URL = console.input("[bold green]Enter the URL to attack: [/bold green]")
    html_content = check_url(URL)

    if html_content == None:
        print("[bold red]Invalid URL[/bold red]")
        break

    info_lab = parse_lab_information(URL)
    print()
    print(Panel(f"""[bold blue]Vulnerability Type: {info_lab[0]}\n \\
                Lab Name: {info_lab[1]}\n \\
                URL: {info_lab[2]}\n \\
                Objective: {info_lab[3]}\n \\
                Dificulty: {info_lab[4]}\n \\
                [/bold blue]", title="Lab Information"""))
        


    

    repeat = input("\nDo you want to check another URL? (y/n): ").lower() == "y"

