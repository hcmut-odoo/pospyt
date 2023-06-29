import time
import json
from requests import Request, Session, exceptions
from .store import Store
from .user import User
from .product import Product
from .order import Order
from .category import Category
from .invoice import Invoice

# installed sub-module
registered_module = {
    "store":Store,
    "category": Category,
    "product": Product,
    "user":User,
    "invoice":Invoice,
    "order": Order
}

class ClientMeta(type):
    def __new__(mcs, name, bases, dct):
        klass = super(ClientMeta, mcs).__new__(mcs, name, bases, dct)
        setattr( klass, "registered_module", registered_module )
        return klass

class Client(object, metaclass=ClientMeta):
    __metaclass__ = ClientMeta

    def __init__(self, api_key, base_url):
        ''' initialize basic params and cache class 
        '''
        self.api_key = api_key
        self.base_url = base_url

        self.CACHED_MODULE = {}
    
    def __getattr__(self, name):
        try:
            value = super(Client, self).__getattribute__(name)
        except AttributeError as e:
            value = self._get_cached_module(name)
            if not value:
                raise e
        return value
        
    def _make_timestamp(self):
        return int(time.time())
    
    def _make_default_parameter(self):
        return {
            "timestamp": self._make_timestamp()
        }

    def _build_request(self, uri, method, body):
        method = method.upper()
        url = self.base_url + "/" + uri
        
        headers = {
            "X-API-Key": self.api_key
        }
        
        req = Request(method, url, headers=headers)

        if body:
            if req.method in ["POST", "PUT", "PATH"]:
                req.json = body
            else:
                req.params = body
        return req

    def _build_response(self, resp):
        '''Decoding JSON - Decode json string to python object
        JSONDecodeError can happen when requests have an HTTP error code like 404 and try to parse the response as JSON
        '''

        if resp.status_code / 100 == 2:
            body = json.loads(resp.text)
        else:
            body = {"request_id": None, "error": resp.status_code, "msg": "http error code"}

        return body
    
    def _get_cached_module(self, key):
        CACHED_MODULE = self.CACHED_MODULE.get(key)

        if not CACHED_MODULE:
            installed = self.registered_module.get(key)
            if not installed:
                return None
            CACHED_MODULE = installed(self)
            self.CACHED_MODULE.setdefault(key, CACHED_MODULE)
        return CACHED_MODULE

    def execute(self, uri, method, body=None):
        ''' defalut timeout value will be 10 seconds
        '''
        parameter = self._make_default_parameter()

        if body.get("timeout"):
            timeout = body.get("timeout")
            body.pop("timeout")
        else:
            timeout = 10 

        if body is not None:
            parameter.update(body)

        request = self._build_request(uri, method, parameter)
        prepped = request.prepare()
        
        session = Session()
        response = session.send(prepped, timeout=timeout)
        response = self._build_response(response)
        return response