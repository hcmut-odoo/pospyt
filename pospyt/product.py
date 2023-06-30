from .base import BaseModule


class Product(BaseModule):
    def create(self, product_data):
        """
        Use this call to add a product.
        :param kwargs:
        :return:
        """
        return self.client._execute("product/create", "POST", product_data)
    
    def read(self, **kwargs):
        """
        Use this call to read a product.
        :param kwargs:
        :return:
        """
        return self.client._execute("product/read", "GET", kwargs)
    
    def delete(self, **kwargs):
        """
        Use this call to delete a product.
        :param kwargs:
        :return:
        """
        return self.client._execute("product/delete", "POST", kwargs)

    def update(self, **kwargs):
        """
        Use this call to delete a product.
        :param kwargs:
        :return:
        """
        return self.client._execute("product/update", "PUT", kwargs)
    
    def list(self, **kwargs):
        """
        Use this call to get a list of categories.
        :param kwargs:
        :return:
        """
        return self.client._execute("product/list", "GET", kwargs)