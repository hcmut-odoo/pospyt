Pospyt v1.0.0
================================


[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/hcmut-odoo/pospyt)
[![Depfu](https://img.shields.io/depfu/depfu/example-ruby.svg)](https://github.com/hcmut-odoo/pospyt)
  

Pos Partners API - python implementation 
---------------------------------------------
This is Python implementation for the [Pos Partner REST API](https://github.com/hcmut-odoo/pos).  


Features
--------
  
- Simple, reliable, and elegant.
- No need to generate authentication and timestamps by yourself, the wrapper does it for you.
- Module format functionality the same as pos officail document.
- Good Response exception handling !
- Have two ways to use, compatible to build Odoo connector with framework OCA/Connector.

Installation
-------
1. Clone repository from github
```shell
git clone https://github.com/hcmut-odoo/pospyt
```

Quick Start
-----------

#### Import wrapper & get list of users
```python
import wrapper
from pprint import pprint

# Using PosWebservice with registed modules
client = wrapper.PosWebservice( BASE_URL, API_KEY )

# Get list of products by price, number of records perpage, page
resp = client.product.lits(per_page=10,page=1)
pprint(resp)

# =================================================

# Using arguments to compatible with the Odoo connector
service = pospyt.PosWebServiceDict(BASE_URL, API_KEY)

# Result of this way always return a dict or a list
# Ids is a list of ids of user from pos website has type int/string 
ids = pos.search('user/list')
pprint(ids)

```

Advance parameters you must want to know
--------

### Timeout

You can find the source code in pospyt.py, and `pospyt` have a timeout params in there.
Hence, every execute funtion can add an extra timeout setting, depending on your choice.

For example, we can set the timeout as 20 seconds in the execute requests(default value is 10s).

```python
resp = client.user.list(per_page=40, page=2, timeout=20)
print(resp)
```

### Pass resource as argument

You can pass resource as argument instead of using registed modules. This way prefers to build the Odoo connector.

Example:
```python
import wrapper
from pprint import pprint

service = pospyt.PosWebServiceDict(BASE_URL, API_KEY)
pprint(pos.search('user/list'))
```

Way to apply on Odoo connector:
```python
class GenericAdapter(AbstractComponent):
    _name = "pos.adapter"
    _inherit = "pos.crud.adapter"

    _model_name = None
    _pos_model = None
    _export_node_name = ""
    _export_node_name_res = ""

    @retryable_error
    def search(self, filters=None):
        """Search records according to some criterias
        and returns a list of ids

        :rtype: list
        """
        _logger.debug(
            "method search, model %s, filters %s", self._pos_model, str(filters)
        )
        return self.client.search(self._pos_model, filters)
```

In this code, you can pass an `resource` as `_pos_model` to method `search`.

Note
----

_Source code_  
    https://github.com/hcmut-odoo/pospyt

_Pos Documentation_  
    https://github.com/hcmut-odoo/pos
