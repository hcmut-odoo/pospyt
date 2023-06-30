import wrapper
from pprint import pprint

API_KEY = ""
BASE_URL = "http://localhost:8000/api"

def main():
    """
    This example call to use wrapper
    """

    # Init pos
    pos = wrapper.PosWebServiceDict(BASE_URL, API_KEY)
    client = wrapper.PosWebservice(BASE_URL, API_KEY)
    # Usecase 1: pass resource as argument
    pprint(pos.search('user/list'))

    pprint("=========================================")

    # Usecase 2: using traditional
    pprint(client.user.list())

if __name__ == "__main__":
    main()


