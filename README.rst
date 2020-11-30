===================
Easy Api Validation
===================

This is a python-package that makes data-validation easier for python developers.
It provides interfaces like Field, IterableField, Validaion etc for validation.

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

Installation
~~~~~~~~~~~~
Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/

Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.5

Mac/Linux
^^^^^^^^^

.. code-block:: sh

    $ pip install ApiValidations==1.0.0

or

.. code-block:: sh

    $ pip install git+https://github.com/soni-vikas/api-validaion.git#egg=api-validation'

Example Usage
~~~~~~~~~~~~~
Validation.validate:
    It will return tuple of length 2: validated_payload, error_flag, validation_status
    In case of any validation failure, the first value will be the error message & the second value will be True.
    In case there are no errors, the first value will be the validated payload, the second value will be False

Field: describes how to validate a field.

IteratorField: subclass of Field, used for a list or any other iterator.

1. Example: Validate literals

.. code:: py

    from api.validations import Validation

    print(Validation.validate("123", int, "user")) # (123, True)

2. Example: Custom validation

.. code:: py

    from api.validations import Validation
    def _check_in_list(x, ls):
        if x not in ls:
            raise ValueError()

        return x

    device = ["cpu", "gpu"]
    print(Validation.validate("cpu", lambda x: _check_in_list(x, device), "device"))
    # ('cpu', False)

    print(Validation.validate("amd", lambda x: _check_in_list(x, device), "device"))
    # ("Field 'device' is in an invalid format.", True)

3. Example: Validation for iterables using Field

.. code:: py

    from api.validations import Validation
    from api.validations import Field, IterableField
    import re

    employee = {
        "name": "vikas soni",
        "phone": "8080808080",
        "org_ids": [
            123,
            345
        ]
    }

    validation_dict = {
        "name": Field(required=True, pattern=re.compile("[a-z]+( [a-z]+)*"), null=True),
        "phone": Field(required=True, pattern=re.compile("^[1-9][0-9]{9}$"), null=True),
        "org_ids": IterableField(required=True, sub_pattern=int)
    }
    payload, error = Validation.validate(employee, validation_dict)
    print(payload)
    print(error)

    # {'name': 'vikas soni', 'phone': '8080808080', 'org_ids': [123, 345]}
    # False

3. Example: Validation for iterables using JSON schema

.. code:: py

    from api.validations import Validation
    import re

    employee = {
        "name": "vikas soni",
        "phone": "8080808080",
        "org_ids": [
            123,
            345
        ]
    }

    validation_dict = {
        "name": {
            'pattern': re.compile(r'[a-z]+( [a-z]+)*'),
            'required': True,
            'null': True
        },
        "phone": {
            'pattern': re.compile("^[1-9][0-9]{9}$"),
            'required': True,
            'null': True
        },
        "org_ids": {
            'pattern': list,
            'required': True,
            'null': False,
            'sub_pattern': int
        }
    }
    payload, error = Validation.validate(employee, validation_dict)
    print(payload)
    print(error)

    # {'name': 'vikas soni', 'phone': '8080808080', 'org_ids': [123, 345]}
    # False

for more examples, see tests cases available in tests/

Development
-----------

Installation
~~~~~~~~~~~~
Assuming that you have Python and ``virtualenv`` installed, set up your
environment and install the required dependencies defined above:

.. code-block:: sh

    $ git clone https://github.com/soni-vikas/api-validaion.git
    $ cd api-validation
    $ virtualenv venv -p python3
    ...
    $ . venv/bin/activate
    $ pip install -e .

Running Tests
~~~~~~~~~~~~~
You can run tests in all supported Python versions using ``python setup.py test``. By default,
it will run all of the unit and functional tests.

.. code-block:: sh

    $ python setup.py test

You can also run individual tests with your default Python version:
see ```--help```.

.. code-block:: sh

    $ python setup.py test --help


For any query raise an issue or create a pull request.