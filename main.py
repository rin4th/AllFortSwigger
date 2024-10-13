from rich.console import Console
from rich import print
from rich.panel import Panel
import platform

from core.utils import RequestLab
from parsers.html_parser import LabParser
from core.attack import run_solver

console = Console()
URL = ""

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

def display_lab_info(info_lab):
    """Display the lab information in a clean format using Rich's Panel."""
    panel_content = f"""
[bold blue]Vulnerability Type: {info_lab[0]}
Lab Name: [bold white]{info_lab[1]}[/bold white]
URL: [bold white]{info_lab[2]}[/bold white]
Objective: [bold white]{info_lab[3]}[/bold white]
Difficulty: [bold white]{info_lab[4]}[/bold white][/bold blue]
    """
    console.print(Panel(panel_content.strip(), title="Lab Information"))

def main_loop():
    """Main function to run the lab attack logic."""
    repeat = True
    clear = "cls" if platform.system() == "Windows" else "clear"

    while repeat:
        print_banner()
        URL = console.input("[bold green]Enter the URL to attack: [/bold green]")
        request_lab = RequestLab(URL)
        valid_url = request_lab.validate_url_lab()

        if not valid_url:
            console.print("[bold red]Invalid URL[/bold red]\n")
            break

        html_content = request_lab.get_html_content()

        lab_parser = LabParser(html_content)
        lab_parser.parse_lab_info()
        info_lab = [lab_parser.get_vulnerability_type(),
                    lab_parser.get_lab_name(),
                    lab_parser.get_lab_link(),
                    lab_parser.get_lab_objective(),
                    lab_parser.get_lab_difficulty()]
        display_lab_info(info_lab)

        if console.input("\n[bold green]Continue with the attack (Y/n)? [/bold green]").lower() != "y":
            break
        
        run_solver(URL, info_lab)

        repeat = input("\nDo you want to check another URL? (y/n): ").lower() == "y"


if __name__ == "__main__":
    main_loop()
