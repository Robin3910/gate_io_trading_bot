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


class Trade(object):
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
        'id': 'str',
        'create_time': 'str',
        'create_time_ms': 'str',
        'currency_pair': 'str',
        'side': 'str',
        'role': 'str',
        'amount': 'str',
        'price': 'str',
        'order_id': 'str',
        'fee': 'str',
        'fee_currency': 'str',
        'point_fee': 'str',
        'gt_fee': 'str',
        'amend_text': 'str',
        'sequence_id': 'str',
        'text': 'str'
    }

    attribute_map = {
        'id': 'id',
        'create_time': 'create_time',
        'create_time_ms': 'create_time_ms',
        'currency_pair': 'currency_pair',
        'side': 'side',
        'role': 'role',
        'amount': 'amount',
        'price': 'price',
        'order_id': 'order_id',
        'fee': 'fee',
        'fee_currency': 'fee_currency',
        'point_fee': 'point_fee',
        'gt_fee': 'gt_fee',
        'amend_text': 'amend_text',
        'sequence_id': 'sequence_id',
        'text': 'text'
    }

    def __init__(self, id=None, create_time=None, create_time_ms=None, currency_pair=None, side=None, role=None, amount=None, price=None, order_id=None, fee=None, fee_currency=None, point_fee=None, gt_fee=None, amend_text=None, sequence_id=None, text=None, local_vars_configuration=None):  # noqa: E501
        # type: (str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, Configuration) -> None
        """Trade - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._create_time = None
        self._create_time_ms = None
        self._currency_pair = None
        self._side = None
        self._role = None
        self._amount = None
        self._price = None
        self._order_id = None
        self._fee = None
        self._fee_currency = None
        self._point_fee = None
        self._gt_fee = None
        self._amend_text = None
        self._sequence_id = None
        self._text = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if create_time is not None:
            self.create_time = create_time
        if create_time_ms is not None:
            self.create_time_ms = create_time_ms
        if currency_pair is not None:
            self.currency_pair = currency_pair
        if side is not None:
            self.side = side
        if role is not None:
            self.role = role
        if amount is not None:
            self.amount = amount
        if price is not None:
            self.price = price
        if order_id is not None:
            self.order_id = order_id
        if fee is not None:
            self.fee = fee
        if fee_currency is not None:
            self.fee_currency = fee_currency
        if point_fee is not None:
            self.point_fee = point_fee
        if gt_fee is not None:
            self.gt_fee = gt_fee
        if amend_text is not None:
            self.amend_text = amend_text
        if sequence_id is not None:
            self.sequence_id = sequence_id
        if text is not None:
            self.text = text

    @property
    def id(self):
        """Gets the id of this Trade.  # noqa: E501

        Trade ID  # noqa: E501

        :return: The id of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Trade.

        Trade ID  # noqa: E501

        :param id: The id of this Trade.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def create_time(self):
        """Gets the create_time of this Trade.  # noqa: E501

        Trading time  # noqa: E501

        :return: The create_time of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this Trade.

        Trading time  # noqa: E501

        :param create_time: The create_time of this Trade.  # noqa: E501
        :type: str
        """

        self._create_time = create_time

    @property
    def create_time_ms(self):
        """Gets the create_time_ms of this Trade.  # noqa: E501

        Trading time, with millisecond precision  # noqa: E501

        :return: The create_time_ms of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._create_time_ms

    @create_time_ms.setter
    def create_time_ms(self, create_time_ms):
        """Sets the create_time_ms of this Trade.

        Trading time, with millisecond precision  # noqa: E501

        :param create_time_ms: The create_time_ms of this Trade.  # noqa: E501
        :type: str
        """

        self._create_time_ms = create_time_ms

    @property
    def currency_pair(self):
        """Gets the currency_pair of this Trade.  # noqa: E501

        Currency pair  # noqa: E501

        :return: The currency_pair of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._currency_pair

    @currency_pair.setter
    def currency_pair(self, currency_pair):
        """Sets the currency_pair of this Trade.

        Currency pair  # noqa: E501

        :param currency_pair: The currency_pair of this Trade.  # noqa: E501
        :type: str
        """

        self._currency_pair = currency_pair

    @property
    def side(self):
        """Gets the side of this Trade.  # noqa: E501

        Order side  # noqa: E501

        :return: The side of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._side

    @side.setter
    def side(self, side):
        """Sets the side of this Trade.

        Order side  # noqa: E501

        :param side: The side of this Trade.  # noqa: E501
        :type: str
        """
        allowed_values = ["buy", "sell"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and side not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `side` ({0}), must be one of {1}"  # noqa: E501
                .format(side, allowed_values)
            )

        self._side = side

    @property
    def role(self):
        """Gets the role of this Trade.  # noqa: E501

        Trade role. No value in public endpoints  # noqa: E501

        :return: The role of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this Trade.

        Trade role. No value in public endpoints  # noqa: E501

        :param role: The role of this Trade.  # noqa: E501
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
    def amount(self):
        """Gets the amount of this Trade.  # noqa: E501

        Trade amount  # noqa: E501

        :return: The amount of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this Trade.

        Trade amount  # noqa: E501

        :param amount: The amount of this Trade.  # noqa: E501
        :type: str
        """

        self._amount = amount

    @property
    def price(self):
        """Gets the price of this Trade.  # noqa: E501

        Order price  # noqa: E501

        :return: The price of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this Trade.

        Order price  # noqa: E501

        :param price: The price of this Trade.  # noqa: E501
        :type: str
        """

        self._price = price

    @property
    def order_id(self):
        """Gets the order_id of this Trade.  # noqa: E501

        Related order ID. No value in public endpoints  # noqa: E501

        :return: The order_id of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this Trade.

        Related order ID. No value in public endpoints  # noqa: E501

        :param order_id: The order_id of this Trade.  # noqa: E501
        :type: str
        """

        self._order_id = order_id

    @property
    def fee(self):
        """Gets the fee of this Trade.  # noqa: E501

        Fee deducted. No value in public endpoints  # noqa: E501

        :return: The fee of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._fee

    @fee.setter
    def fee(self, fee):
        """Sets the fee of this Trade.

        Fee deducted. No value in public endpoints  # noqa: E501

        :param fee: The fee of this Trade.  # noqa: E501
        :type: str
        """

        self._fee = fee

    @property
    def fee_currency(self):
        """Gets the fee_currency of this Trade.  # noqa: E501

        Fee currency unit. No value in public endpoints  # noqa: E501

        :return: The fee_currency of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._fee_currency

    @fee_currency.setter
    def fee_currency(self, fee_currency):
        """Sets the fee_currency of this Trade.

        Fee currency unit. No value in public endpoints  # noqa: E501

        :param fee_currency: The fee_currency of this Trade.  # noqa: E501
        :type: str
        """

        self._fee_currency = fee_currency

    @property
    def point_fee(self):
        """Gets the point_fee of this Trade.  # noqa: E501

        Points used to deduct fee. No value in public endpoints  # noqa: E501

        :return: The point_fee of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._point_fee

    @point_fee.setter
    def point_fee(self, point_fee):
        """Sets the point_fee of this Trade.

        Points used to deduct fee. No value in public endpoints  # noqa: E501

        :param point_fee: The point_fee of this Trade.  # noqa: E501
        :type: str
        """

        self._point_fee = point_fee

    @property
    def gt_fee(self):
        """Gets the gt_fee of this Trade.  # noqa: E501

        GT used to deduct fee. No value in public endpoints  # noqa: E501

        :return: The gt_fee of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._gt_fee

    @gt_fee.setter
    def gt_fee(self, gt_fee):
        """Sets the gt_fee of this Trade.

        GT used to deduct fee. No value in public endpoints  # noqa: E501

        :param gt_fee: The gt_fee of this Trade.  # noqa: E501
        :type: str
        """

        self._gt_fee = gt_fee

    @property
    def amend_text(self):
        """Gets the amend_text of this Trade.  # noqa: E501

        The custom data that the user remarked when amending the order  # noqa: E501

        :return: The amend_text of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._amend_text

    @amend_text.setter
    def amend_text(self, amend_text):
        """Sets the amend_text of this Trade.

        The custom data that the user remarked when amending the order  # noqa: E501

        :param amend_text: The amend_text of this Trade.  # noqa: E501
        :type: str
        """

        self._amend_text = amend_text

    @property
    def sequence_id(self):
        """Gets the sequence_id of this Trade.  # noqa: E501

        Represents a unique and consecutive trade ID within a single market. It is used to track and identify trades in the specific market  # noqa: E501

        :return: The sequence_id of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._sequence_id

    @sequence_id.setter
    def sequence_id(self, sequence_id):
        """Sets the sequence_id of this Trade.

        Represents a unique and consecutive trade ID within a single market. It is used to track and identify trades in the specific market  # noqa: E501

        :param sequence_id: The sequence_id of this Trade.  # noqa: E501
        :type: str
        """

        self._sequence_id = sequence_id

    @property
    def text(self):
        """Gets the text of this Trade.  # noqa: E501

        User defined information. No value in public endpoints  # noqa: E501

        :return: The text of this Trade.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this Trade.

        User defined information. No value in public endpoints  # noqa: E501

        :param text: The text of this Trade.  # noqa: E501
        :type: str
        """

        self._text = text

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
        if not isinstance(other, Trade):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Trade):
            return True

        return self.to_dict() != other.to_dict()
