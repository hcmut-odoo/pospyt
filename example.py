import pospyt
from pprint import pprint

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

    options = {
        'filter':filters,
        'display': display,
        'sort': sort,
        'limit': 2,
        'date': date
    }

    # Search method only return list of ids
    pprint(pos.search('product/list', options=options))

    # Result
    # [23, 25]

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

if __name__ == "__main__":
    main()


