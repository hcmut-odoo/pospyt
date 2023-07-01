from .base import BaseModule


class Category(BaseModule):
    def create(self, category_data):
        """
        Use this call to add a product category.
        :param category_data:
        :return:
        """
        return self.client._execute("category/create", "POST", category_data)
    
    def read(self, options=None):
        """
        Use this call to read a product category.
        :param options:
        :return:
        """
        return self.client._execute("category/read", "GET", options)
    
    def delete(self, options=None):
        """
        Use this call to delete a product category.
        :param options:
        :return:
        """
        return self.client._execute("category/delete", "POST", options)

    def update(self, options=None):
        """
        Use this call to delete a product category.
        :param options:
        :return:
        """
        return self.client._execute("category/update", "PUT", options)
    
    def list(self, options=None):
        """
        Use this call to get a list of product categories.
        :param options:
        :return:
        """
        return self.client._execute("category/list", "GET", options)