from .base import BaseModule


class Product(BaseModule):
    def create(self, product_data):
        """
        Use this call to add a product.
        :param options:
        :return:
        """
        return self.client._execute("product", "POST", "create", product_data)
    
    def read(self, options=None):
        """
        Use this call to read a product.
        :param options:
        :return:
        """
        return self.client._execute("product", "GET", "read", options)
    
    def delete(self, options=None):
        """
        Use this call to delete a product.
        :param options:
        :return:
        """
        return self.client._execute("product", "POST", "delete", options)

    def update(self, options=None):
        """
        Use this call to delete a product.
        :param options:
        :return:
        """
        return self.client._execute("product", "PUT", "update", options)
    
    def list(self, options=None):
        """
        Use this call to get a list of categories.
        :param options:
        :return:
        """
        return self.client._execute("product", "GET", "list", options)