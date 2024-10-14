from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich import box 
from halo import Halo
import string


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
        self.console.log(f"Requesting {self.url}")
        request = RequestLab(self.url)
        
        if method == 'GET':
            self.html_content = request.request_get()
        # elif method == 'POST':
        #     self.html_content = request.request_post()
        # elif method == 'PUT':
        #     self.html_content = request.request_put()
        # elif method == 'DELETE':
        #     self.html_content = request.request_delete()
        
        self.__set_soup_html()

    def _print_table(self, title, headers, rows):
        """Print a table."""
        table = Table(title=title, box=box.SIMPLE)
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*row)
        self.console.print(table)

    def __set_soup_html(self):
        """Set the soup HTML."""
        self.console.log("Parsing HTML content")
        self.soup_html = BeautifulSoup(self.html_content.text, 'html.parser')
    
    def _print_payload(self, payload):
        """Print the payload."""
        ascii_char = string.ascii_letters + string.digits + string.punctuation
        payload_char = ""
        spinner = Halo(text=ascii_char, spinner='dots')
        spinner.start()
        for char in payload:
            payload_char += char
            spinner.text = payload_char
            


        

    @abstractmethod
    def build_payload():
        """Build the payload."""
        pass

    @abstractmethod
    def solve(self):
        """Solve the lab."""
        pass    
    

        
        
