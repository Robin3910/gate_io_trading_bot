# coding: utf-8

"""
    Gate API v4

    Welcome to Gate.io API  APIv4 provides spot, margin and futures trading operations. There are public APIs to retrieve the real-time market statistics, and private APIs which needs authentication to trade on user's behalf.  # noqa: E501

    Contact: support@mail.gate.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from gate_api.configuration import Configuration


class FuturesTrade(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'int',
        'create_time': 'float',
        'create_time_ms': 'float',
        'contract': 'str',
        'size': 'int',
        'price': 'str',
        'is_internal': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'create_time': 'create_time',
        'create_time_ms': 'create_time_ms',
        'contract': 'contract',
        'size': 'size',
        'price': 'price',
        'is_internal': 'is_internal'
    }

    def __init__(self, id=None, create_time=None, create_time_ms=None, contract=None, size=None, price=None, is_internal=None, local_vars_configuration=None):  # noqa: E501
        # type: (int, float, float, str, int, str, bool, Configuration) -> None
        """FuturesTrade - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._create_time = None
        self._create_time_ms = None
        self._contract = None
        self._size = None
        self._price = None
        self._is_internal = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if create_time is not None:
            self.create_time = create_time
        if create_time_ms is not None:
            self.create_time_ms = create_time_ms
        if contract is not None:
            self.contract = contract
        if size is not None:
            self.size = size
        if price is not None:
            self.price = price
        if is_internal is not None:
            self.is_internal = is_internal

    @property
    def id(self):
        """Gets the id of this FuturesTrade.  # noqa: E501

        Trade ID  # noqa: E501

        :return: The id of this FuturesTrade.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FuturesTrade.

        Trade ID  # noqa: E501

        :param id: The id of this FuturesTrade.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def create_time(self):
        """Gets the create_time of this FuturesTrade.  # noqa: E501

        Trading time  # noqa: E501

        :return: The create_time of this FuturesTrade.  # noqa: E501
        :rtype: float
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this FuturesTrade.

        Trading time  # noqa: E501

        :param create_time: The create_time of this FuturesTrade.  # noqa: E501
        :type: float
        """

        self._create_time = create_time

    @property
    def create_time_ms(self):
        """Gets the create_time_ms of this FuturesTrade.  # noqa: E501

        Trading time, with milliseconds set to 3 decimal places.  # noqa: E501

        :return: The create_time_ms of this FuturesTrade.  # noqa: E501
        :rtype: float
        """
        return self._create_time_ms

    @create_time_ms.setter
    def create_time_ms(self, create_time_ms):
        """Sets the create_time_ms of this FuturesTrade.

        Trading time, with milliseconds set to 3 decimal places.  # noqa: E501

        :param create_time_ms: The create_time_ms of this FuturesTrade.  # noqa: E501
        :type: float
        """

        self._create_time_ms = create_time_ms

    @property
    def contract(self):
        """Gets the contract of this FuturesTrade.  # noqa: E501

        Futures contract  # noqa: E501

        :return: The contract of this FuturesTrade.  # noqa: E501
        :rtype: str
        """
        return self._contract

    @contract.setter
    def contract(self, contract):
        """Sets the contract of this FuturesTrade.

        Futures contract  # noqa: E501

        :param contract: The contract of this FuturesTrade.  # noqa: E501
        :type: str
        """

        self._contract = contract

    @property
    def size(self):
        """Gets the size of this FuturesTrade.  # noqa: E501

        Trading size  # noqa: E501

        :return: The size of this FuturesTrade.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this FuturesTrade.

        Trading size  # noqa: E501

        :param size: The size of this FuturesTrade.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def price(self):
        """Gets the price of this FuturesTrade.  # noqa: E501

        Trading price (quote currency)  # noqa: E501

        :return: The price of this FuturesTrade.  # noqa: E501
        :rtype: str
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this FuturesTrade.

        Trading price (quote currency)  # noqa: E501

        :param price: The price of this FuturesTrade.  # noqa: E501
        :type: str
        """

        self._price = price

    @property
    def is_internal(self):
        """Gets the is_internal of this FuturesTrade.  # noqa: E501

        Whether internal trade. Internal trade refers to the takeover of liquidation orders by the insurance fund and ADL users. Since it is not a normal matching on the market depth, the transaction price may deviate, and it will not be recorded in the K-line. If it is not an internal trade, this field will not be returned.  # noqa: E501

        :return: The is_internal of this FuturesTrade.  # noqa: E501
        :rtype: bool
        """
        return self._is_internal

    @is_internal.setter
    def is_internal(self, is_internal):
        """Sets the is_internal of this FuturesTrade.

        Whether internal trade. Internal trade refers to the takeover of liquidation orders by the insurance fund and ADL users. Since it is not a normal matching on the market depth, the transaction price may deviate, and it will not be recorded in the K-line. If it is not an internal trade, this field will not be returned.  # noqa: E501

        :param is_internal: The is_internal of this FuturesTrade.  # noqa: E501
        :type: bool
        """

        self._is_internal = is_internal

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FuturesTrade):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FuturesTrade):
            return True

        return self.to_dict() != other.to_dict()
