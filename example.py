import wrapper

API_KEY = ""
BASE_URL = "http://localhost:8000/api"

def main():
    """
    This example call to get list products
    :param kwargs:
    :return:
    """

    # Init client
    client = wrapper.Client(API_KEY, BASE_URL)

    # Call an api
    # resp is an object of dictionary type
    resp = client.product.list(per_page=5, page=1)

    # Print resp after convert to dictionary
    print(resp)

if __name__ == "__main__":
    main()


