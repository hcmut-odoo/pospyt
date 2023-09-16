import pospyt
from pprint import pprint
from datetime import datetime

API_KEY = ""
BASE_URL = "http://localhost:8000/api"

def main():
    """
    This example call to use wrapper
    """

    # Init pos
    pos = pospyt.PosWebServiceDict(BASE_URL, API_KEY)
    client = pospyt.PosWebservice(BASE_URL, API_KEY)

    # Usecase 1: pass resource as argument
    filters = {
        'price': {'operator': 'lt', 'value': 40000}
    }

    display = ['name', 'price', 'updated_at']
    sort = {'price': 'asc'}
    date = {
        'start': '2021-10-20', 
        'end': '2021-11-20'
    }

    date_format = '%Y-%m-%d'

    date = {
        'start': datetime.strptime('2021-10-20', date_format),
        'end': datetime.strptime('2021-11-20', date_format)
    }

    options = {
        'filter':filters,
        'display': display,
        'sort': sort,
        'limit': 2,
        'date': date,
        'action': 'list'
    }

    # GET METHOD
    # ==========================================================
    # Search method only return list of ids
    pprint(pos.search('product', options=options))

    # List method return list of data
    pprint(pos.list('product', options=options))

    # Find method return data of an reousrce id
    pprint(pos.find('product', 1))

    pprint("=========================================")

    # Usecase 2: using registed modules
    pprint(client.product.list(options=options))
    
    # Result
    # [
    #     {
    #         'id': 23,
    #         'name': 'Cà Phê Đen Đá',
    #         'price': '32000.00',
    #         'updated_at': '2021-11-11T15:09:29.000000Z'
    #     },
    #     {
    #         'id': 25,
    #         'name': 'Cà Phê Sữa Đá',
    #         'price': '32000.00',
    #         'updated_at': '2021-11-11T15:09:29.000000Z'
    #     }
    # ]
    # ==========================================================

    # POST METHOD
    # ==========================================================
    update_order_options = {
        'action': 'reject',
        'id': 4
    }

    pprint(pos.add('order', options=update_order_options))
    # ==========================================================

if __name__ == "__main__":
    main()


