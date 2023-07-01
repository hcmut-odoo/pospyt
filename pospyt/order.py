from .base import BaseModule


class Order(BaseModule):
    def create(self, order_data):
        """
        Use this call to add an order.
        :param order_data:
        :return:
        """
        return self.client._execute("order/create", "POST", order_data)
    
    def read(self, options=None):
        """
        Use this call to read an order.
        :param options:
        :return:
        """
        return self.client._execute("order/read", "GET", options)
    
    def delete(self, options=None):
        """
        Use this call to delete an order.
        :param options:
        :return:
        """
        return self.client._execute("order/delete", "POST", options)

    def update(self, options=None):
        """
        Use this call to delete an order.
        :param options:
        :return:
        """
        return self.client._execute("order/update", "PUT", options)
    
    def list(self, options=None):
        """
        Use this call to get a list of product categories.
        :param options:
        :return:
        """
        return self.client._execute("order/list", "GET", options)