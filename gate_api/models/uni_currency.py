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


class UniCurrency(object):
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
        'currency': 'str',
        'min_lend_amount': 'str',
        'max_lend_amount': 'str',
        'max_rate': 'str',
        'min_rate': 'str'
    }

    attribute_map = {
        'currency': 'currency',
        'min_lend_amount': 'min_lend_amount',
        'max_lend_amount': 'max_lend_amount',
        'max_rate': 'max_rate',
        'min_rate': 'min_rate'
    }

    def __init__(self, currency=None, min_lend_amount=None, max_lend_amount=None, max_rate=None, min_rate=None, local_vars_configuration=None):  # noqa: E501
        # type: (str, str, str, str, str, Configuration) -> None
        """UniCurrency - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._currency = None
        self._min_lend_amount = None
        self._max_lend_amount = None
        self._max_rate = None
        self._min_rate = None
        self.discriminator = None

        if currency is not None:
            self.currency = currency
        if min_lend_amount is not None:
            self.min_lend_amount = min_lend_amount
        if max_lend_amount is not None:
            self.max_lend_amount = max_lend_amount
        if max_rate is not None:
            self.max_rate = max_rate
        if min_rate is not None:
            self.min_rate = min_rate

    @property
    def currency(self):
        """Gets the currency of this UniCurrency.  # noqa: E501

        Currency name  # noqa: E501

        :return: The currency of this UniCurrency.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this UniCurrency.

        Currency name  # noqa: E501

        :param currency: The currency of this UniCurrency.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def min_lend_amount(self):
        """Gets the min_lend_amount of this UniCurrency.  # noqa: E501

        The minimum lending amount, in the unit of the currency.  # noqa: E501

        :return: The min_lend_amount of this UniCurrency.  # noqa: E501
        :rtype: str
        """
        return self._min_lend_amount

    @min_lend_amount.setter
    def min_lend_amount(self, min_lend_amount):
        """Sets the min_lend_amount of this UniCurrency.

        The minimum lending amount, in the unit of the currency.  # noqa: E501

        :param min_lend_amount: The min_lend_amount of this UniCurrency.  # noqa: E501
        :type: str
        """

        self._min_lend_amount = min_lend_amount

    @property
    def max_lend_amount(self):
        """Gets the max_lend_amount of this UniCurrency.  # noqa: E501

        The total maximum lending amount, in USDT  # noqa: E501

        :return: The max_lend_amount of this UniCurrency.  # noqa: E501
        :rtype: str
        """
        return self._max_lend_amount

    @max_lend_amount.setter
    def max_lend_amount(self, max_lend_amount):
        """Sets the max_lend_amount of this UniCurrency.

        The total maximum lending amount, in USDT  # noqa: E501

        :param max_lend_amount: The max_lend_amount of this UniCurrency.  # noqa: E501
        :type: str
        """

        self._max_lend_amount = max_lend_amount

    @property
    def max_rate(self):
        """Gets the max_rate of this UniCurrency.  # noqa: E501

        Maximum rate (Hourly)  # noqa: E501

        :return: The max_rate of this UniCurrency.  # noqa: E501
        :rtype: str
        """
        return self._max_rate

    @max_rate.setter
    def max_rate(self, max_rate):
        """Sets the max_rate of this UniCurrency.

        Maximum rate (Hourly)  # noqa: E501

        :param max_rate: The max_rate of this UniCurrency.  # noqa: E501
        :type: str
        """

        self._max_rate = max_rate

    @property
    def min_rate(self):
        """Gets the min_rate of this UniCurrency.  # noqa: E501

        Minimum rate (Hourly)  # noqa: E501

        :return: The min_rate of this UniCurrency.  # noqa: E501
        :rtype: str
        """
        return self._min_rate

    @min_rate.setter
    def min_rate(self, min_rate):
        """Sets the min_rate of this UniCurrency.

        Minimum rate (Hourly)  # noqa: E501

        :param min_rate: The min_rate of this UniCurrency.  # noqa: E501
        :type: str
        """

        self._min_rate = min_rate

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
        if not isinstance(other, UniCurrency):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UniCurrency):
            return True

        return self.to_dict() != other.to_dict()
