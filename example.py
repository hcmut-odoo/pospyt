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
    pprint(pos.search('user/list'))

    pprint("=========================================")

    # Usecase 2: using registed modules
    pprint(client.user.list())

if __name__ == "__main__":
    main()


