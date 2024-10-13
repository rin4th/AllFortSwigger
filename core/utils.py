import requests
import json
from bs4 import BeautifulSoup


class RequestLab:
    def __init__(self, URL):
        self.url = URL
        self.html_content = None

    def validate_url_lab(self):
        """Validate the URL of the lab."""
        valid_url = self.request_get()
        if not valid_url:
            return False
        soup = BeautifulSoup(self.html_content.text, 'html.parser')
        title = soup.head.title.text

        json_parser = JSONParser()
        list_vuln = json_parser.get_list_vuln() 

        for vuln in list_vuln:
            for lab in vuln['listLab']:
                if lab['name'] in title:
                    return True
        return False
         
    def request_get(self):
        """Make a GET request to the lab URL."""
        try:
            self.html_content = requests.get(self.url)
            if self.html_content.status_code != 200:
                return None
            return True
        except Exception as e:
            return None
    
        
class JSONParser:
    def __init__(self):
        self.json_data = None
        
    def get_json_data(self):
        """Read the JSON"""
        path = '/mnt/project/ctf/portSwigger/AllFortSwigger/config/labs.json'
        with open(path, 'r') as file:
            self.json_data = json.load(file)
            file.close()
    
    def get_list_vuln(self):
        """Return the list of vulnerabilities."""
        if self.json_data is None:
            self.get_json_data()
        return self.json_data['listVuln']
