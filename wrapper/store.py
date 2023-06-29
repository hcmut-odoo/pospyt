from .base import BaseModule


class Store(BaseModule):
    def create(self, store_data):
        """
        Use this call to add a store.
        :param kwargs:
        :return:
        """
        return self.client.execute("store/create", "POST", store_data)
    
    def read(self, **kwargs):
        """
        Use this call to read a store.
        :param kwargs:
        :return:
        """
        return self.client.execute("store/read", "GET", kwargs)
    
    def delete(self, **kwargs):
        """
        Use this call to delete a store.
        :param kwargs:
        :return:
        """
        return self.client.execute("store/delete", "POST", kwargs)

    def update(self, **kwargs):
        """
        Use this call to delete a store.
        :param kwargs:
        :return:
        """
        return self.client.execute("store/update", "PUT", kwargs)
    
    def list(self, **kwargs):
        """
        Use this call to get a list of categories.
        :param kwargs:
        :return:
        """
        return self.client.execute("store/list", "GET", kwargs)