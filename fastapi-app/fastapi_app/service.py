from model import ProductModel


class ProductService:
    def __init__(self):
        self.model = ProductModel()

    def create(self, params):
        return self.model.create(
            params["name"], params["description"], params["quantity"], params["price"]
        )

    def read(self):
        return self.model.read()
