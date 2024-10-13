from rich.console import Console
from rich import print
import platform
import importlib

from utils import retrieve_json_data


console = Console()
clear = "cls" if platform.system() == "Windows" else "clear"

def run_solver(URL, info_lab):

    lab_data = retrieve_json_data()

    for vuln in lab_data['listVuln']:
        if vuln['vulnName'] == info_lab[0]:
            for lab in vuln['listLab']:
                if lab['name'] == info_lab[1]:
                    solver_class_name = lab['solverClass']
                    
                    module_path = f"vulnerabilities.sql_injection.{solver_class_name}"
                    module = importlib.import_module(module_path)
                    
                    solver_class = getattr(module, solver_class_name)
                    
                    solver = solver_class()
                    solver.solve(URL)
                    return  # Exit after solving the lab

            
            # If the lab name is not found
            print(f"Lab name '{info_lab[1]}' not found for {info_lab[0]}")
            return


    print(f"Starting attack on {URL}")
    




