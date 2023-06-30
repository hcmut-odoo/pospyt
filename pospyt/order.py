from .base import BaseModule


class Order(BaseModule):
    def create(self, order_data):
        """
        Use this call to add an order.
        :param kwargs:
        :return:
        """
        return self.client._execute("order/create", "POST", order_data)
    
    def read(self, **kwargs):
        """
        Use this call to read an order.
        :param kwargs:
        :return:
        """
        return self.client._execute("order/read", "GET", kwargs)
    
    def delete(self, **kwargs):
        """
        Use this call to delete an order.
        :param kwargs:
        :return:
        """
        return self.client._execute("order/delete", "POST", kwargs)

    def update(self, **kwargs):
        """
        Use this call to delete an order.
        :param kwargs:
        :return:
        """
        return self.client._execute("order/update", "PUT", kwargs)
    
    def list(self, **kwargs):
        """
        Use this call to get a list of product categories.
        :param kwargs:
        :return:
        """
        return self.client._execute("order/list", "GET", kwargs)