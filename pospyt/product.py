from .base import BaseModule


class Product(BaseModule):
    def create(self, product_data):
        """
        Use this call to add a product.
        :param options:
        :return:
        """
        return self.client._execute("product/create", "POST", product_data)
    
    def read(self, options=None):
        """
        Use this call to read a product.
        :param options:
        :return:
        """
        return self.client._execute("product/read", "GET", options)
    
    def delete(self, options=None):
        """
        Use this call to delete a product.
        :param options:
        :return:
        """
        return self.client._execute("product/delete", "POST", options)

    def update(self, options=None):
        """
        Use this call to delete a product.
        :param options:
        :return:
        """
        return self.client._execute("product/update", "PUT", options)
    
    def list(self, options=None):
        """
        Use this call to get a list of categories.
        :param options:
        :return:
        """
        print(options)
        return self.client._execute("product/list", "GET", options)