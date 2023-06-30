from .base import BaseModule


class Category(BaseModule):
    def create(self, category_data):
        """
        Use this call to add a product category.
        :param kwargs:
        :return:
        """
        return self.client._execute("category/create", "POST", category_data)
    
    def read(self, **kwargs):
        """
        Use this call to read a product category.
        :param kwargs:
        :return:
        """
        return self.client._execute("category/read", "GET", kwargs)
    
    def delete(self, **kwargs):
        """
        Use this call to delete a product category.
        :param kwargs:
        :return:
        """
        return self.client._execute("category/delete", "POST", kwargs)

    def update(self, **kwargs):
        """
        Use this call to delete a product category.
        :param kwargs:
        :return:
        """
        return self.client._execute("category/update", "PUT", kwargs)
    
    def list(self, **kwargs):
        """
        Use this call to get a list of product categories.
        :param kwargs:
        :return:
        """
        return self.client._execute("category/list", "GET", kwargs)