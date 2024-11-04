from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class UnionQueryRetrieveDataSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)

    def solve(self):
        """Solve the lab."""
        self.determine_DBMS()
        self.determine_column_number()
        self.determine_DB_version()
        self.retrieve_table_name()
        self.retrieve_column_name()
        self.retrieve_data()
        self.request_login(allow_redirects=False)
        self._print_solved()

    def custom_payload(self):
        """Build the payload."""
        pass