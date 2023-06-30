from .base import BaseModule


class User(BaseModule):
    def create(self, user_data):
        """
        Use this call to add a user.
        :param kwargs:
        :return:
        """
        return self.client._execute("user/create", "POST", user_data)
    
    def read(self, **kwargs):
        """
        Use this call to read a user.
        :param kwargs:
        :return:
        """
        return self.client._execute("user/read", "GET", kwargs)
    
    def delete(self, **kwargs):
        """
        Use this call to delete a user.
        :param kwargs:
        :return:
        """
        return self.client._execute("user/delete", "POST", kwargs)

    def update(self, **kwargs):
        """
        Use this call to delete a user.
        :param kwargs:
        :return:
        """
        return self.client._execute("user/update", "PUT", kwargs)
    
    def list(self, **kwargs):
        """
        Use this call to get a list of categories.
        :param kwargs:
        :return:
        """
        return self.client._execute("user/list", "GET", kwargs)