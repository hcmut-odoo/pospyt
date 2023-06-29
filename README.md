pyshopee v1.3.9
================================


[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/hcmut-odoo/pos-wrapper)
[![Depfu](https://img.shields.io/depfu/depfu/example-ruby.svg)](https://github.com/hcmut-odoo/pos-wrapper)
  

Pos Partners API - python implementation 
---------------------------------------------
This is Python implementation for the [Pos Partner REST API](https://github.com/hcmut-odoo/pos).  

```python
import wrapper

client = wrapper.Client( BASE_URL, API_KEY )

# get_order_by_status (UNPAID/READY_TO_SHIP/SHIPPED/COMPLETED/CANCELLED/ALL)
resp = client.order.get_order_by_status(order_status="READY_TO_SHIP")
print(resp)
# Get list of products (record_per_page=10,page=1)
resp = client.product.list(per_page=5, page=1)
```
Features
--------
  
- Simple, reliable, and elegant.
- No need to generate authentication and timestamps by yourself, the wrapper does it for you.
- Module format functionality the same as pos officail document.
- Good Response exception handling !


Installation
-------
1. Clone repository from github
```shell
git clone https://github.com/hcmut-odoo/pos-wrapper
```

Quick Start
-----------

#### Import wrapper & get list of users
```python
import wrapper

client = wrapper.Client( BASE_URL, API_KEY )

# Get list of users by default per_page=10,page=1
resp = client.user.list()
print(resp)
```

Advance parameters you must want to know
--------

### Timeout

You can find the source code in client.py, and `wrapper` have a timeout params in there.
Hence, every execute funtion can add an extra timeout setting, depending on your choice.

```python

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
```

For example, we can set the timeout as 20 seconds in the execute requests(default value is 10s).

```python
resp = client.user.list(per_page=40, page=2, timeout=20)
print(resp)
```

  
Note
----

_Source code_  
    https://github.com/hcmut-odoo/pos-wrapper

_Pos Documentation_  
    https://github.com/hcmut-odoo/pos
