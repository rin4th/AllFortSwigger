from bs4 import BeautifulSoup
import requests

from core.utils import JSONParser

class LabParser:
    def __init__(self, html_content):
        self.html_content = html_content
        self.name_lab = None
        self.lab_link = None
        self.objective_lab = None
        self.difficulty = None
        self.type_vuln = None

    def fetch_lab_page(self):
        """Fetch the lab page and return the BeautifulSoup object."""
        return BeautifulSoup(self.html_content.text, 'html.parser')
    
    def fetch_lab_page_info(self):
        """Fetch the lab info page and return the BeautifulSoup object."""
        response = requests.get(self.lab_link)
        return BeautifulSoup(response.text, 'html.parser')
    

    def parse_lab_info(self):
        """Main method to parse lab info, objective, difficulty, and type."""
        soup = self.fetch_lab_page()
        
        self.lab_link = self.get_lab_link(soup)
        soup_lab_info = self.fetch_lab_page_info()

        self.name_lab = self.get_lab_name(soup)
        self.objective_lab = self.get_lab_objective(soup_lab_info)
        self.difficulty = self.get_lab_difficulty(soup_lab_info)
        self.type_vuln = self.get_vulnerability_type()

        return self.type_vuln, self.name_lab, self.lab_link, self.objective_lab, self.difficulty
    
    def get_lab_name(self, soup):
        """Extract the lab name from the page."""
        return soup.head.title.text

    def get_lab_link(self, soup):
        """Extract the link to the lab."""
        link = soup.find('a', class_='link-back')
        if link:
            return link['href']
        return None

    def get_lab_objective(self, soup_lab_info):
        """Retrieve the objective of the lab."""
        paragraphs = soup_lab_info.find_all('p')

        for p in paragraphs:
            if "To solve the lab" in p.get_text():
                return p.get_text()[31:-9]

        return None

    def get_lab_difficulty(self, soup_lab_info):
        """Retrieve the difficulty of the lab and format it."""
        p_dif = soup_lab_info.find('p', class_='widget-container-labelevel')
        difficulty = p_dif.find('span').get_text()

        if difficulty == "APPRENTICE":
            return r"[bold green]APPRENTICE[/bold green]"
        elif difficulty == "PRACTITIONER":
            return r"[bold yellow]PRACTITIONER[/bold yellow]"
        else:
            return r"[bold red]EXPERT[/bold red]"

    def get_vulnerability_type(self):
        """Retrieve the vulnerability type based on the lab name."""
        json_parser = JSONParser()
        list_vuln = json_parser.get_list_vuln()
        for vuln in list_vuln:
            for lab in vuln['listLab']:
                if lab['name'] == self.name_lab:
                    return vuln['nameVuln']

        return None