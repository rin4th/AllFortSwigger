from rich.console import Console
from rich import print
import platform
import importlib

from core.utils import JSONParser


console = Console()
clear = "cls" if platform.system() == "Windows" else "clear"

def run_solver(URL, info_lab):

    json_parser = JSONParser()
    list_vuln = json_parser.get_list_vuln()

    for vuln in list_vuln:
        if vuln['nameVuln'] == info_lab[0]:
            for lab in vuln['listLab']:
                if lab['name'] == info_lab[1]:
                    solver_class_name = lab['solverClass']
                    module_name = lab['module_name']
                    
                    module_path = f"services.sql_injection.labs.{module_name}"
                    module = importlib.import_module(module_path)
                    
                    solver_class = getattr(module, solver_class_name)
                    
                    solver = solver_class(URL)
                    solver.solve()
                    return

    print(f"Lab name '{info_lab[1]}' not found for {info_lab[0]}")
    return


    print(f"Starting attack on {URL}")
    




