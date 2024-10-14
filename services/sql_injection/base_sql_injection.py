from abc import ABC, abstractmethod

from core.utils import RequestLab


class SQLInjectionBaseSolver(ABC):
    def __init__(self, url):
        self.url = url
        self.html_content = None

        self.__set_html_content()

    def __set_html_content(self):
        """Return the RequestLab object."""
        request = RequestLab(self.url)
        self.html_content = request.request_get()

    def get_html_content(self):
        """Return the HTML content of the lab."""
        return self.html_content

    @abstractmethod
    def build_payload():
        """Build the payload."""
        pass

    @abstractmethod
    def solve(self):
        """Solve the lab."""
        pass    
    

        
        
