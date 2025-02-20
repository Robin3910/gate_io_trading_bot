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


class MyFuturesTradeTimeRange(object):
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
        'trade_id': 'str',
        'create_time': 'float',
        'contract': 'str',
        'order_id': 'str',
        'size': 'int',
        'close_size': 'int',
        'price': 'str',
        'role': 'str',
        'text': 'str',
        'fee': 'str',
        'point_fee': 'str'
    }

    attribute_map = {
        'trade_id': 'trade_id',
        'create_time': 'create_time',
        'contract': 'contract',
        'order_id': 'order_id',
        'size': 'size',
        'close_size': 'close_size',
        'price': 'price',
        'role': 'role',
        'text': 'text',
        'fee': 'fee',
        'point_fee': 'point_fee'
    }

    def __init__(self, trade_id=None, create_time=None, contract=None, order_id=None, size=None, close_size=None, price=None, role=None, text=None, fee=None, point_fee=None, local_vars_configuration=None):  # noqa: E501
        # type: (str, float, str, str, int, int, str, str, str, str, str, Configuration) -> None
        """MyFuturesTradeTimeRange - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._trade_id = None
        self._create_time = None
        self._contract = None
        self._order_id = None
        self._size = None
        self._close_size = None
        self._price = None
        self._role = None
        self._text = None
        self._fee = None
        self._point_fee = None
        self.discriminator = None

        if trade_id is not None:
            self.trade_id = trade_id
        if create_time is not None:
            self.create_time = create_time
        if contract is not None:
            self.contract = contract
        if order_id is not None:
            self.order_id = order_id
        if size is not None:
            self.size = size
        if close_size is not None:
            self.close_size = close_size
        if price is not None:
            self.price = price
        if role is not None:
            self.role = role
        if text is not None:
            self.text = text
        if fee is not None:
            self.fee = fee
        if point_fee is not None:
            self.point_fee = point_fee

    @property
    def trade_id(self):
        """Gets the trade_id of this MyFuturesTradeTimeRange.  # noqa: E501

        Trade ID  # noqa: E501

        :return: The trade_id of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: str
        """
        return self._trade_id

    @trade_id.setter
    def trade_id(self, trade_id):
        """Sets the trade_id of this MyFuturesTradeTimeRange.

        Trade ID  # noqa: E501

        :param trade_id: The trade_id of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: str
        """

        self._trade_id = trade_id

    @property
    def create_time(self):
        """Gets the create_time of this MyFuturesTradeTimeRange.  # noqa: E501

        Trading time  # noqa: E501

        :return: The create_time of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: float
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this MyFuturesTradeTimeRange.

        Trading time  # noqa: E501

        :param create_time: The create_time of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: float
        """

        self._create_time = create_time

    @property
    def contract(self):
        """Gets the contract of this MyFuturesTradeTimeRange.  # noqa: E501

        Futures contract  # noqa: E501

        :return: The contract of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: str
        """
        return self._contract

    @contract.setter
    def contract(self, contract):
        """Sets the contract of this MyFuturesTradeTimeRange.

        Futures contract  # noqa: E501

        :param contract: The contract of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: str
        """

        self._contract = contract

    @property
    def order_id(self):
        """Gets the order_id of this MyFuturesTradeTimeRange.  # noqa: E501

        Order ID related  # noqa: E501

        :return: The order_id of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this MyFuturesTradeTimeRange.

        Order ID related  # noqa: E501

        :param order_id: The order_id of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: str
        """

        self._order_id = order_id

    @property
    def size(self):
        """Gets the size of this MyFuturesTradeTimeRange.  # noqa: E501

        Trading size  # noqa: E501

        :return: The size of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this MyFuturesTradeTimeRange.

        Trading size  # noqa: E501

        :param size: The size of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def close_size(self):
        """Gets the close_size of this MyFuturesTradeTimeRange.  # noqa: E501

        Number of closed positions:  close_size=0 && size＞0       Open long position close_size=0 && size＜0       Open short position close_size>0 && size>0 && size <= close_size Close short postion close_size>0 && size>0 && size > close_size Close short position and open long position close_size<0 && size<0 && size >= close_size Close long postion close_size<0 && size<0 && size < close_size Close long position and open short position  # noqa: E501

        :return: The close_size of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: int
        """
        return self._close_size

    @close_size.setter
    def close_size(self, close_size):
        """Sets the close_size of this MyFuturesTradeTimeRange.

        Number of closed positions:  close_size=0 && size＞0       Open long position close_size=0 && size＜0       Open short position close_size>0 && size>0 && size <= close_size Close short postion close_size>0 && size>0 && size > close_size Close short position and open long position close_size<0 && size<0 && size >= close_size Close long postion close_size<0 && size<0 && size < close_size Close long position and open short position  # noqa: E501

        :param close_size: The close_size of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: int
        """

        self._close_size = close_size

    @property
    def price(self):
        """Gets the price of this MyFuturesTradeTimeRange.  # noqa: E501

        Trading price  # noqa: E501

        :return: The price of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: str
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this MyFuturesTradeTimeRange.

        Trading price  # noqa: E501

        :param price: The price of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: str
        """

        self._price = price

    @property
    def role(self):
        """Gets the role of this MyFuturesTradeTimeRange.  # noqa: E501

        Trade role. Available values are `taker` and `maker`  # noqa: E501

        :return: The role of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this MyFuturesTradeTimeRange.

        Trade role. Available values are `taker` and `maker`  # noqa: E501

        :param role: The role of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: str
        """
        allowed_values = ["taker", "maker"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and role not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `role` ({0}), must be one of {1}"  # noqa: E501
                .format(role, allowed_values)
            )

        self._role = role

    @property
    def text(self):
        """Gets the text of this MyFuturesTradeTimeRange.  # noqa: E501

        User defined information  # noqa: E501

        :return: The text of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this MyFuturesTradeTimeRange.

        User defined information  # noqa: E501

        :param text: The text of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: str
        """

        self._text = text

    @property
    def fee(self):
        """Gets the fee of this MyFuturesTradeTimeRange.  # noqa: E501

        Fee deducted  # noqa: E501

        :return: The fee of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: str
        """
        return self._fee

    @fee.setter
    def fee(self, fee):
        """Sets the fee of this MyFuturesTradeTimeRange.

        Fee deducted  # noqa: E501

        :param fee: The fee of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: str
        """

        self._fee = fee

    @property
    def point_fee(self):
        """Gets the point_fee of this MyFuturesTradeTimeRange.  # noqa: E501

        Points used to deduct fee  # noqa: E501

        :return: The point_fee of this MyFuturesTradeTimeRange.  # noqa: E501
        :rtype: str
        """
        return self._point_fee

    @point_fee.setter
    def point_fee(self, point_fee):
        """Sets the point_fee of this MyFuturesTradeTimeRange.

        Points used to deduct fee  # noqa: E501

        :param point_fee: The point_fee of this MyFuturesTradeTimeRange.  # noqa: E501
        :type: str
        """

        self._point_fee = point_fee

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
        if not isinstance(other, MyFuturesTradeTimeRange):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MyFuturesTradeTimeRange):
            return True

        return self.to_dict() != other.to_dict()
