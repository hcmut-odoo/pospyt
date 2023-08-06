from .base import BaseModule


class User(BaseModule):
    def create(self, user_data):
        """
        Use this call to add a user.
        :param user_data:
        :return:
        """
        return self.client._execute("user", "POST", "create", user_data)
    
    def read(self, options=None):
        """
        Use this call to read a user.
        :param options:
        :return:
        """
        return self.client._execute("user", "GET", "read", options)
    
    def delete(self, options=None):
        """
        Use this call to delete a user.
        :param options:
        :return:
        """
        return self.client._execute("user", "POST", "delete", options)

    def update(self, options=None):
        """
        Use this call to delete a user.
        :param options:
        :return:
        """
        return self.client._execute("user", "PUT", "update", options)
    
    def list(self, options=None):
        """
        Use this call to get a list of categories.
        :param options:
        :return:
        """
        return self.client._execute("user", "GET", "list", options)