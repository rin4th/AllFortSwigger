from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class UnionQueryNumberColumnsSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)

    def solve(self):
        """Solve the lab."""
        self.determine_DBMS()
        self.determine_column_number()
        self._print_solved()

    def build_payload(self):
        """Build the payload."""
        pass