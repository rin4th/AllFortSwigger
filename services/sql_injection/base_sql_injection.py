from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich import box 
from rich import print
from halo import Halo
import time



from core.utils import RequestLab


class SQLInjectionBaseSolver(ABC):
    def __init__(self, url):
        self.console = Console()
        self.url = url
        self.html_content = None
        self.soup_html = None
        self.payload = None

    def _request_lab(self, method='GET'):
        """Return the RequestLab object."""
        request = RequestLab(self.url)
        
        if method == 'GET':
            request.request_get()
            self.html_content = request.get_html_content()
        # elif method == 'POST':
        #     self.html_content = request.request_post()
        # elif method == 'PUT':
        #     self.html_content = request.request_put()
        # elif method == 'DELETE':
        #     self.html_content = request.request_delete()
        time.sleep(0.5)
        self.__set_soup_html()

    def _print_table(self, title, headers, rows):
        """Print a table."""
        table = Table(title=title, box=box.ROUNDED)
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*row)
        self.console.log(table)

    def __set_soup_html(self):
        """Set the soup HTML."""
        self.soup_html = BeautifulSoup(self.html_content.text, 'html.parser')
        time.sleep(0.5)
    
    def _print_payload(self, payload):
        """Print the payload."""
        payload_char = ""
        spinner = Halo(text=payload_char, spinner='dots', interval=1000)
        spinner.start()
        for char in payload:
            time.sleep(0.3)
            payload_char += char
            spinner.text = payload_char
        spinner.stop()
            
    def _print_solved(self):
        """Print the solved message."""
        print(r"""[bold green]
        .-------------------------------------.
        |  ____   ___  _ __     _______ ____  |
        | / ___| / _ \| |\ \   / / ____|  _ \ |
        | \___ \| | | | | \ \ / /|  _| | | | ||
        |  ___) | |_| | |__\ V / | |___| |_| ||
        | |____/ \___/|_____\_/  |_____|____/ |
        |                                     |
        '-------------------------------------' [/bold green]
""")

    @abstractmethod
    def build_payload():
        """Build the payload."""
        pass

    @abstractmethod
    def solve(self):
        """Solve the lab."""
        pass    
    

        
        
