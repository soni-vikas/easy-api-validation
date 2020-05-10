import unittest, re
from typing import List
from api.validations import Validation
from api.validations import Field, IterableField
from api.validations import ValidationError


def _check_in_list(x, ls: List):
    if x not in ls:
        raise ValueError()

    return x

class ValidationsTestCase(unittest.TestCase):

    def test_raise_exception_true(self):
        with self.assertRaises(ValidationError) as e:
            print(e)
            employee = {
                "name": "Vikas 123",
            }
            validation_dict = {
                'name': {
                    "pattern": re.compile("^[a-z]+( [a-z]+)*$")
                }
            }
            Validation.validate(employee, validation_dict, raise_exception=True)

    def tests_required_fields(self):
        employee = {
        }
        validation_dict = {
            'name': {
                "required": True,
                "pattern": re.compile("^[a-z]+( [a-z]+)*$")
            }
        }
        message, error = Validation.validate(employee, validation_dict)
        assert error == True
        assert message == "Field 'name' is required but not provided."

    def tests_default_fields(self):
        employee = {
        }
        validation_dict = {
            'group': {
                "default": "A",
                "pattern": lambda x: _check_in_list(x, ["A", "B", "C", "D"])
            }
        }
        payload, error = Validation.validate(employee, validation_dict, raise_exception=True)
        assert error == False
        self.assertDictEqual(payload, {"group": 'A'})

    def tests_invalid_format(self):
        employee = {
            "phone": "783",
            "name": "123 abc",
        }
        validation_dict = {
            'phone': {
                "required": True,
                "pattern": re.compile("^[1-9][0-9]{9}$")
            },
            'name': {
                "required": True,
                "pattern": re.compile("^[a-z]+( [a-z]+)*$")
            }
        }
        message, error = Validation.validate(employee, validation_dict)
        assert error == True
        assert message == "Fields 'name', 'phone' are in an invalid format."

    def test_null(self):
        employee = {
            "phone": "7838329012",
            "name": "vikas soni",
            "email": None,
            "uid": "1234"
        }
        validation_dict = {
            'phone': {
                "required": True,
                "pattern": re.compile("^[1-9][0-9]{9}$")
            },
            'name': {
                "required": True,
                "pattern": re.compile("^[a-z]+( [a-z]+)*$")
            },
            "email": {
                "null": True,
                "pattern": str
            },
            "uid": {
                "pattern": int
            }
        }

        payload, error = Validation.validate(employee, validation_dict)
        assert error == False, payload
        self.assertDictEqual(payload, {
            "phone": "7838329012",
            "name": "vikas soni",
            "email": None,
            "uid": 1234
        })

    def test_iterable(self):
        employee = {
            "name": "vikas soni",
            "organizations": [
                {
                    "name": "tech",
                    "org_id": 1234
                },
                {
                    "name": "ml",
                    "org_id": "5678"
                },
                {
                    "name": "operations",
                    "org_id": 9101
                },
                {
                    "name": None,
                    "org_id": 1121
                },
            ]
        }
        name_dict = Field(required=True, pattern=lambda x: _check_in_list(x, ["tech", "ml", "operations"]), null=True)
        validation_dict = {
            "name": Field(required=True, pattern=re.compile("[a-z]+( [a-z]+)*"), null=True),
            "organizations": IterableField(required=True, sub_pattern={
                "name": name_dict,
                "org_id": Field(pattern=int),
            })
        }
        payload, error = Validation.validate(employee, validation_dict)
        assert error == False, payload

        self.assertDictEqual(payload, {
            "name": "vikas soni",
            "organizations": [
                {
                    "name": "tech",
                    "org_id": 1234
                },
                {
                    "name": "ml",
                    "org_id": 5678
                },
                {
                    "name": "operations",
                    "org_id": 9101
                },
                {
                    "name": None,
                    "org_id": 1121
                },
            ]
        })

    def test_iterable_with_literals(self):
        employee = {
            "name": "vikas soni",
            "org_ids": [
                123,
                245
            ]
        }
        validation_dict = {
            "name": Field(required=True, pattern=re.compile("[a-z]+( [a-z]+)*"), null=True),
            "org_ids": IterableField(required=True, sub_pattern=int)
        }
        payload, error = Validation.validate(employee, validation_dict)
        assert error == False, payload
        self.assertDictEqual(payload, employee)

    def test_iterable_with_literals_using_json(self):
        employee = {
            "name": "vikas soni",
            "org_ids": [
                123,
                245
            ]
        }
        validation_dict = {
            "name": {
                'pattern': re.compile(r'[a-z]+( [a-z]+)*'),
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
        assert error == False, payload
        self.assertDictEqual(payload, employee)

    def test_iterable_with_literals_fail(self):
        employee = {
            "name": "vikas soni",
            "org_ids": [
                123,
                "abcdef"
            ]
        }
        validation_dict = {
            "name": Field(required=True, pattern=re.compile("[a-z]+( [a-z]+)*"), null=True),
            "org_ids": IterableField(required=True, sub_pattern=int)
        }
        payload, error = Validation.validate(employee, validation_dict)
        assert error == True
        assert payload == "Field 'org_ids.1' is in an invalid format."

    def test_check_literals_pass(self):
        payload, error = Validation.validate("123", int)
        assert error == False
        assert payload == 123

    def test_check_literals_fail(self):
        payload, error = Validation.validate("abc", int)
        assert error == True
        assert payload == "Field 'None' is in an invalid format.", payload


        payload, error = Validation.validate("vikas", int, "user")
        assert error == True
        assert payload == "Field 'user' is in an invalid format.", payload