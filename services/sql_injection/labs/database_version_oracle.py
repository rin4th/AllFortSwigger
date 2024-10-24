from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class DatabaseVersionOracleSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)

    def solve(self):
        """Solve the lab."""
        self.determine_DBMS()
        self.determine_column_number()
        self.determine_DB_version()
        self._print_solved()

    def build_payload(self):
        """Build the payload."""
        pass 
