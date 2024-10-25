import requests
import json
from bs4 import BeautifulSoup
import logging


class RequestLab:
    def __init__(self, URL):
        self.url = URL
        self.html_content = None
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        self.headers = None

        self.session = requests.Session()

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
    
    def get_html_content(self):
        """Return the HTML content of the lab."""
        return self.html_content
         
    def request_get(self, cookies=None):
        """Make a GET request to the lab URL."""
        try:
            self.html_content = self.session.get(self.url, cookies=cookies)
            return True
        except Exception as e:
            return None
        
    def request_post(self, data=None, cookies=None, allow_redirects=True):
        """Make a POST request to the lab URL."""
        try:
            self.html_content = self.session.post(self.url, data=data,
                                                  cookies=cookies, headers=self.headers,
                                                  allow_redirects=allow_redirects)

        except Exception as e:
            print("An error occurred:", e)
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

class JSONPayloadSQLInjection:
    def __init__(self):
        self.json_data = None

    def get_json_data(self):
        """Read the JSON"""
        path = '/mnt/project/ctf/portSwigger/AllFortSwigger/services/sql_injection/dbms.json'
        with open(path, 'r') as file:
            self.json_data = json.load(file)
            file.close()
    
    def get_list_dbms(self):
        """Return the list of DBMS."""
        if self.json_data is None:
            self.get_json_data()
        return self.json_data['list_dbms']