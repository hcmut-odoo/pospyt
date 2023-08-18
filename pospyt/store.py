from .base import BaseModule


class Store(BaseModule):
    def create(self, store_data):
        """
        Use this call to add a store.
        :param store_data:
        :return:
        """
        return self.client._execute("store", "POST", "create", store_data)
    
    def read(self, options):
        """
        Use this call to read a store.
        :param options:
        :return:
        """
        return self.client._execute("store", "GET", "read", options)
    
    def delete(self, options):
        """
        Use this call to delete a store.
        :param options:
        :return:
        """
        return self.client._execute("store", "POST", "delete", options)

    def update(self, options):
        """
        Use this call to delete a store.
        :param options:
        :return:
        """
        return self.client._execute("store", "PUT", "update", options)
    
    def list(self, options):
        """
        Use this call to get a list of categories.
        :param options:
        :return:
        """
        return self.client._execute("store", "GET", "list", options)