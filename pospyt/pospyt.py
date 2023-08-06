import time
import json
from requests import Request, Session, exceptions
from http.client import HTTPConnection
from urllib.parse import urlencode
import mimetypes
from bs4 import BeautifulSoup
import datetime

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

class PosWebServiceError(Exception):
    """Generic Pos WebServices error class.

    To catch these, you need to import it in you code e.g. :
    from prestapyt import PrestaShopWebServiceError
    """

    def __init__(self, msg, error_code=None,
                 ps_error_msg='', ps_error_code=None):
        """Intiliaze webservice error."""
        self.msg = msg
        self.error_code = error_code
        self.ps_error_msg = ps_error_msg
        self.ps_error_code = ps_error_code

    def __str__(self):
        """Include custom msg."""
        return repr(self.ps_error_msg or self.msg)

class PosAuthenticationError(PosWebServiceError):
    pass

class PosWebservice(object, metaclass=ClientMeta):
    __metaclass__ = ClientMeta

    def __init__(self, base_url, api_key, debug=False, session=None,
                 verbose=False):
        """
        Create an instance of PrestashopWebService.

        In your code, you can use :
        from prestapyt import PrestaShopWebService, PrestaShopWebServiceError

        try:
            posClient = PosWebService(
                'http://localhost:8000/api',
                'BVWPFFYBT97WKM959D7AVVD0M4815Y1L'
            )
        except PosWebServiceError as err:
            ...

        When verbose mode is activated, you might need to activate the
        debug logging for the logger "requests.packages.urllib3"::

          logger = logging.getLogger("requests.packages.urllib3")
          logger.setLevel(logging.DEBUG)

        The verbose logging will show the requests, including headers and data,
        and the responses with headers but no data.

        :param base_url: Root URL for the shop
        :param api_key: Authentification key
        :param debug: activate Pos's webservice debug mode
        :param session: pass a custom requests Session
        :param verbose: activate logging of the requests/responses (but no
        responses body)
        """
        self._api_key = api_key
        self._base_url = base_url

        # optional arguments
        self.debug = debug
        self.verbose = verbose

        if session is None:
            self.client = Session()
        else:
            self.client = session

        if not self.client.auth:
            self.client.auth = (api_key, '')

        self.CACHED_MODULE = {}
    
    def __getattr__(self, name):
        try:
            value = super(PosWebservice, self).__getattribute__(name)
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

    def _build_request(self, uri, method, action, headers, data):
        method = method.upper()
        url = ""
        base_url = self._base_url
 
        if base_url.endswith('/'):
            url = base_url + uri
        else:
            url = base_url + '/' + uri
        
        if action is not None:
            url = f"{url}/{action}"
        
        authenticate_headers = {
            "X-API-Key": self._api_key
        }
        
        if headers is not None:
            headers.update(authenticate_headers)
        
        request = Request(method, url, headers=headers)

        if data:
            if request.method in ["POST", "PUT", "PATCH"]:
                request.json = data
            elif isinstance(data, dict):
                request.json = data
            else:
                request.params = data
        
        print(request.params)
        return request

    def _get_cached_module(self, key):
        CACHED_MODULE = self.CACHED_MODULE.get(key)

        if not CACHED_MODULE:
            installed = self.registered_module.get(key)
            if not installed:
                return None
            CACHED_MODULE = installed(self)
            self.CACHED_MODULE.setdefault(key, CACHED_MODULE)
        return CACHED_MODULE

    def _parse_error(self, content):
        """Take the JSON content as a dictionary and extract the PrestaShop error.

        :param json_content: JSON content returned by the PS server as a dictionary
        :return: (pos_error_code, prestashop_error_message)
        """
        if isinstance(content, dict):
            error_content = (
                content.get('pos', {})
                    .get('errors', {})
                    .get('error', {})
            )
            if isinstance(error_content, list):
                error_content = error_content[0]
            code = error_content.get('code')
            message = error_content.get('title')
            return (code, message)
        else:
            # Assuming the content is in HTML format (Laravel)
            # Extract the error message from the HTML content
            soup = BeautifulSoup(content, 'html.parser')
            title_tag = soup.title
            if title_tag is not None:
                error_message = title_tag.string
            else:
                error_message = None
            return (None, error_message)

    def _check_status_code(self, status_code, content):
        """Take the status code and check it.

        Throw an exception if the server didn't return 200 or 201 code.

        :param status_code: status code returned by the server
        :return: True or raise an exception PrestaShopWebServiceError
        """
        message_by_code = {204: 'No content',
                           400: 'Bad Request',
                           401: 'Unauthorized',
                           404: 'Not Found',
                           405: 'Method Not Allowed',
                           500: 'Internal Server Error',
                           }
        if status_code in (200, 201):
            return True
        elif status_code == 401:
            # the content is empty for auth errors
            raise PosAuthenticationError(
                message_by_code[status_code],
                status_code
            )
        elif status_code in message_by_code:
            ps_error_code, ps_error_msg = self._parse_error(content)
            raise PosWebServiceError(
                message_by_code[status_code],
                status_code,
                ps_error_msg=ps_error_msg,
                ps_error_code=ps_error_code,
            )
        else:
            ps_error_code, ps_error_msg = self._parse_error(content)
            raise PosWebServiceError(
                'Unknown error',
                status_code,
                ps_error_msg=ps_error_msg,
                ps_error_code=ps_error_code,
            )
    
    def _parse(self, content):
        """Parse the response of the webservice.

        :param content: response from the webservice
        :return: an json object of the content
        """
        if not content:
            raise PosWebServiceError('HTTP response is empty')

        try:
            parsed_content = json.loads(content)
        except json.JSONDecodeError as err:
            raise PosWebServiceError(
                'HTTP Json response is not parsable : %s' % (err,)
            )

        return parsed_content
    
    def _build_response(self, method, resp):
        """
        Decoding JSON - Decode JSON string to Python object
        JSONDecodeError can happen when requests have an HTTP error code 
        like 404 and try to parse the response as JSON
        """

        if method == "HEAD":
            if resp.status_code / 100 == 2:
                return resp.headers
            else:
                return {"request_id": None, "error": resp.status_code, "msg": "HTTP error code"}

        if resp.status_code / 100 == 2:
            body = self._parse(resp.text)
        else:
            body = {"request_id": None, "error": resp.status_code, "msg": "HTTP error code"}

        return body

    def _validate_query_options(self, options):
        """Check options against supported options.

        :param options: dict of options to use for the request
        :return: True if valid, else raise an error PrestaShopWebServiceError

        Official ref:
        https://github.com/hcmut-odoo/pospyt
        """

        if not isinstance(options, dict):
            raise PosWebServiceError(
                'Parameters must be a instance of dict'
            )
        supported = (
            'filter', 'display', 'sort', 'date', 'limit', 'page', 'action', 'id'
        )

        unsupported = set([
            param.split('[')[0]
            for param in options
        ]).difference(supported)

        if unsupported:
            raise PosWebServiceError(
                'Unsupported parameters: %s' % (', '.join(tuple(unsupported)),)
            )
        return True
    
    def _make_default_option():
        return {
                'limit': 10,
                'page': 1
            }

    def _execute(self, uri, method, action, data=None, add_headers=None):
        """Execute a request on the PrestaShop Webservice.

        :param url: full URL to call
        :param method: GET, POST, PUT, DELETE, HEAD
        :param body: for PUT (edit) and POST (add) only,
                        the JSON data sent to PrestaShop
        :param add_headers: additional headers merged onto instance's headers.
        :return: tuple with (status code, header, content) of the response.
        """
        parameter = self._make_default_parameter()

        method_with_default_options = ["GET", "HEAD"]
        if data is None and method in method_with_default_options:
            data = self._make_default_option()

        if data is not None:
            timeout = data.get("timeout", 10)
        else:
            timeout = 10

        if data is not None:
            data.update(parameter)
        if self.debug:
            data.update({'debug': True})

        if add_headers is None:
            add_headers = {}

        request_headers = self.client.headers.copy()
        request_headers.update(add_headers)

        request = self._build_request(
            uri,
            method,
            action,
            headers=request_headers,
            data=data
        )

        if self.verbose:
            currentlevel = HTTPConnection.debuglevel
            HTTPConnection.debuglevel = 1
        try:
            prepped = request.prepare()
            response = self.client.send(prepped, timeout=timeout)
        finally:
            if self.verbose:
                HTTPConnection.debuglevel = currentlevel

        self._check_status_code(response.status_code, response.content)
        response = self._build_response(method, response)

        return response

    def _encode_multipart_formdata(self, files):
        """Encode files to an http multipart/form-data.

        :param files: a sequence of (type, filename, value)
            elements for data to be uploaded as files.
        :return: headers and body.
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = b'\r\n'
        L = []
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append(
                'Content-Disposition: form-data; \
                    name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        L = map(lambda l: l if isinstance(l, bytes) else l.encode('utf-8'), L)
        body = CRLF.join(L)
        headers = {
            'Content-Type': 'multipart/form-data; boundary=%s' % BOUNDARY
        }
        return headers, body
    
    def _get_content_type(self, filename):
        """Retrieve filename mimetype.

        :param filename: file name.
        :return: mimetype.
        """
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    def search(self, resource, options=None):
        """Retrieve (GET) a resource and return the json with the ids.

        This method is only a mapper to the get method
        without the resource_id, but semantically
        it is more clear than "get without id" to search resources

        :param resource: string of the resource
            to search like 'category', 'products'
        :param options: optional dict of parameters to filter the search
            (one or more of 'filter', 'display', 'sort', 'limit', 'page')
        :return: the response as a dict
        """
        return self.get(resource, options=options)

    def get(self, resource, resource_id=None, options=None):
        """Retrieve (GET) a resource.

        :param resource: type of resource to retrieve
        :param resource_id: optional resource id to retrieve
        :param kwargs: Optional dict of parameters (one or more of
                        'filter', 'display', 'sort', 'limit', 'page')
        :return: the response as a dict
        """
        if options is not None:
            self._validate_query_options(options)
        if resource_id is not None:
            options.update({'id': resource_id})
        if options.get('action') is not None:
            action = options.get('action')
        else:
            raise PosWebServiceError(
                f"Options of GET {resource} must have a specific action"
            )

        return self._execute(uri=resource, method='GET', action=action, data=options)
    
    def head(self, resource, resource_id=None, options={}):
        """Head method (HEAD) a resource.

        :param resource: type of resource to retrieve
        :param resource_id: optional resource id to retrieve
        :param options: optional dict of parameters
            (one or more of 'filter', 'display', 'sort', 'limit', 'page')
        :return: the header of the response as a dict
        """
        if options is not None:
            self._validate_query_options(options)
        if resource_id is not None:
            options.update({'id': resource_id})
        if options.get('action') is not None:
            action = options.get('action')
        else:
            raise PosWebServiceError(
                f"Options of HEAD {resource} must have a specific action"
            )
        
        return self._execute(uri=resource, method='HEAD', action=action, data=options)
    
    def add(self, resource, files=None, options={}):
        """Add (POST) a resource. Content can be a dict of values to create.

        :param resource: type of resource to create
        :param files: a sequence of (type, filename, value) elements
            for data to be uploaded as files.
        :param options: dict of options to use for the request
        :return: the response as a dict
        """

        if options is not None:
            self._validate_query_options(options)

        if options.get('action') is not None:
                action = options.get('action')
        else:
            raise PosWebServiceError(
                f"Options of POST {resource} must have a specific action"
            )

        if files is not None:
            multipart_data = []
            for file_data in files:
                file_type, filename, value = file_data
                multipart_data.append(('files[]', (filename, value, file_type)))

            if options is not None:
                multipart_data.append(('data', json.dumps(options)))
            
            return self._execute(url=resource, method='POST', action=action, data=multipart_data)

        elif options is not None:
            return self._execute(url=resource, method='POST', action=action, data=options)

        else:
            raise PosWebServiceError('Undefined data.')

            
    def edit(self, resource, content, options={}):
        """Edit (PUT) a resource.

        :param resource: type of resource to edit
        :param content: modified data as dict of the resource.
        :return: the response as a dict
        """
        if options:
            self._validate_query_options(options)
        if content is not None:
            options.update(content)
        if options.get('action') is not None:
                action = options.get('action')
        else:
            raise PosWebServiceError(
                f"Options of UPDATE {resource} must have a specific action"
            )
        
        return self._execute(uri=resource, method='POST', action=action, data=options)
    
    def delete(self, resource, resource_ids):
        """Delete (DELETE) a resource.

        :param resource: type of resource to delete
        :param resource_ids: int or list of IDs to delete
        :return: True if delete is done,
            raise an error PosWebServiceError if missed
        """
        if isinstance(resource_ids, (tuple, list)):
            body = {'id': resource_ids}
        else:
            body = {'id': [resource_ids]}

        return self._execute(uri=resource, method='DELETE', action='delete', data=body)

    def connect(self, resource):
        """Check (POST) a connection.

        :param resource: path of resource to check
        :return: True if check is done,
            raise an error PosWebServiceError if missed
        """
        return self._execute(uri=resource, method='POST')

class PosWebServiceDict(PosWebservice):
    """Interacts with the Pos WebService API, use dict for messages."""

    def search(self, resource, options=None):
        """Retrieve (GET) a resource and return a list of its ids.

        Is not supposed to be called with an id
        or whatever in the resource line 'addresses/1'
        But only with 'addresses' or 'products' etc...

        :param resource: string of the resource to search like,
            ie: 'addresses', 'products', 'manufacturers', etc.
        :param kwargs: optional dict of parameters to filter the search
            (one or more of 'filter', 'display', 'sort', 'limit', 'page')
        :return: list of ids as int/string
        """
        def _parse_php_unique_id(unique_id):
            return str(unique_id)

        response = super(PosWebServiceDict, self).search(resource, options)
        data = response
        
        if isinstance(response, dict):
            data = response.get('data', [])

        ids = []

        for item in data:
            try:
                # Try converting to integer
                id_value = int(item['id'])
            except ValueError:
                # Fallback to alternate parsing method
                id_value = _parse_php_unique_id(item['id'])
            ids.append(id_value)

        return ids

    def partial_add(self, resource, fields):
        """Add (POST) a resource without necessary all the content.

        Retrieve the full empty envelope
        and merge the given fields in this envelope.

        :param resource: type of resource to create
        :param fields: dict of fields of the resource to create
        :return: response of the server
        """
        blank_envelope = self.get(resource, options={'page': 'blank'})
        complete_content = dict(blank_envelope, **fields)
        return self.add(resource=resource, options=complete_content)
    
    def partial_edit(self, resource, resource_id, fields):
        """Edit (PUT) partially a resource.

        Standard REST PUT means a full replacement of the resource.
        Allows to edit only only some fields of the resource with
        a perf penalty. It will read on prestashop,
        then modify the keys in content,
        and write on prestashop.

        :param resource: type of resource to edit
        :param resource_id: id of the resource to edit
        :param fields: dict containing the field name as key
            and the values of the files to modify
        :return: the response as a dict
        """
        complete_content = self.get(resource, resource_id)
        for key in complete_content:
            if fields.get(key):
                complete_content[key].update(fields[key])
        return self.edit(resource, complete_content)

