from .base import BaseModule


class Invoice(BaseModule):
    def create(self, invoice_data):
        """
        Use this call to add an invoice.
        :param invoice_data:
        :return:
        """
        return self.client._execute("invoice", "create", "POST", invoice_data)
    
    def read(self, options=None):
        """
        Use this call to read an invoice.
        :param options:
        :return:
        """
        return self.client._execute("invoice", "read", "GET", options)
    
    def delete(self, options=None):
        """
        Use this call to delete an invoice.
        :param options:
        :return:
        """
        return self.client._execute("invoice", "delete", "POST", options)

    def update(self, options=None):
        """
        Use this call to delete an invoice.
        :param options:
        :return:
        """
        return self.client._execute("invoice", "update", "PUT", options)
    
    def list(self, options=None):
        """
        Use this call to get a list of categories.
        :param options:
        :return:
        """
        return self.client._execute("invoice", "list", "GET", options)