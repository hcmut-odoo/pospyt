from .base import BaseModule


class Invoice(BaseModule):
    def create(self, invoice_data):
        """
        Use this call to add an invoice.
        :param kwargs:
        :return:
        """
        return self.client._execute("invoice/create", "POST", invoice_data)
    
    def read(self, **kwargs):
        """
        Use this call to read an invoice.
        :param kwargs:
        :return:
        """
        return self.client._execute("invoice/read", "GET", kwargs)
    
    def delete(self, **kwargs):
        """
        Use this call to delete an invoice.
        :param kwargs:
        :return:
        """
        return self.client._execute("invoice/delete", "POST", kwargs)

    def update(self, **kwargs):
        """
        Use this call to delete an invoice.
        :param kwargs:
        :return:
        """
        return self.client._execute("invoice/update", "PUT", kwargs)
    
    def list(self, **kwargs):
        """
        Use this call to get a list of categories.
        :param kwargs:
        :return:
        """
        return self.client._execute("invoice/list", "GET", kwargs)