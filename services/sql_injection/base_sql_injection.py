from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich import box 
from rich import print
import time



from core.utils import RequestLab


class SQLInjectionBaseSolver(ABC):
    def __init__(self, url):
        self.console = Console()
        self.url = url
        self.html_content = None
        self.soup_html = None
        self.payload = None

    def _request_lab(self, method='GET', data=None, cookies=None):
        """Return the RequestLab object."""
        request = RequestLab(self.url)
        
        if method == 'GET':
            request.request_get()
            self.html_content = request.get_html_content()
        elif method == 'POST':
            request.request_post(data, cookies)
            self.html_content = request.get_html_content()
        # elif method == 'PUT':
        #     self.html_content = request.request_put()
        # elif method == 'DELETE':
        #     self.html_content = request.request_delete()
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
        self.console.print("Payload: ", payload)
            
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
        
    def determine_DBMS(self):
        """Determine the DBMS."""
        pass

    def determine_column_number(self):
        """Determine the number of columns."""
        pass

    def finding_data_type_column(self):
        """Finding the data type of the column."""
        pass


    def determine_DB_version(self):
        """Determine the DB version."""
        pass

    def retrieve_DB_name(self):
        """Retrieve the DB name."""
        pass

    def retrieve_table_name(self):
        """Retrieve the table name."""
        pass

    def retrieve_column_name(self):
        """Retrieve the column name."""
        pass
    
    def retrieve_data(self):
        """Retrieve the data."""
        pass

    @abstractmethod
    def build_payload():
        """Build the payload."""
        pass

    @abstractmethod
    def solve(self):
        """Solve the lab."""
        pass    
    

        
        
