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


class UnifiedPortfolioOutput(object):
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
        'maintain_margin_total': 'str',
        'initial_margin_total': 'str',
        'calculate_time': 'int',
        'risk_unit': 'list[MockRiskUnit]'
    }

    attribute_map = {
        'maintain_margin_total': 'maintain_margin_total',
        'initial_margin_total': 'initial_margin_total',
        'calculate_time': 'calculate_time',
        'risk_unit': 'risk_unit'
    }

    def __init__(self, maintain_margin_total=None, initial_margin_total=None, calculate_time=None, risk_unit=None, local_vars_configuration=None):  # noqa: E501
        # type: (str, str, int, list[MockRiskUnit], Configuration) -> None
        """UnifiedPortfolioOutput - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._maintain_margin_total = None
        self._initial_margin_total = None
        self._calculate_time = None
        self._risk_unit = None
        self.discriminator = None

        if maintain_margin_total is not None:
            self.maintain_margin_total = maintain_margin_total
        if initial_margin_total is not None:
            self.initial_margin_total = initial_margin_total
        if calculate_time is not None:
            self.calculate_time = calculate_time
        if risk_unit is not None:
            self.risk_unit = risk_unit

    @property
    def maintain_margin_total(self):
        """Gets the maintain_margin_total of this UnifiedPortfolioOutput.  # noqa: E501

        Total maintenance margin, including only the portfolio margin calculation results for positions in the risk unit,  excluding borrowed margin. If borrowing exists, conventional borrowing margin requirements will still apply.  # noqa: E501

        :return: The maintain_margin_total of this UnifiedPortfolioOutput.  # noqa: E501
        :rtype: str
        """
        return self._maintain_margin_total

    @maintain_margin_total.setter
    def maintain_margin_total(self, maintain_margin_total):
        """Sets the maintain_margin_total of this UnifiedPortfolioOutput.

        Total maintenance margin, including only the portfolio margin calculation results for positions in the risk unit,  excluding borrowed margin. If borrowing exists, conventional borrowing margin requirements will still apply.  # noqa: E501

        :param maintain_margin_total: The maintain_margin_total of this UnifiedPortfolioOutput.  # noqa: E501
        :type: str
        """

        self._maintain_margin_total = maintain_margin_total

    @property
    def initial_margin_total(self):
        """Gets the initial_margin_total of this UnifiedPortfolioOutput.  # noqa: E501

        Total initial margin, calculated as the maximum of the following three combinations: position,  position + positive delta orders, position + negative delta orders.  # noqa: E501

        :return: The initial_margin_total of this UnifiedPortfolioOutput.  # noqa: E501
        :rtype: str
        """
        return self._initial_margin_total

    @initial_margin_total.setter
    def initial_margin_total(self, initial_margin_total):
        """Sets the initial_margin_total of this UnifiedPortfolioOutput.

        Total initial margin, calculated as the maximum of the following three combinations: position,  position + positive delta orders, position + negative delta orders.  # noqa: E501

        :param initial_margin_total: The initial_margin_total of this UnifiedPortfolioOutput.  # noqa: E501
        :type: str
        """

        self._initial_margin_total = initial_margin_total

    @property
    def calculate_time(self):
        """Gets the calculate_time of this UnifiedPortfolioOutput.  # noqa: E501

        Calculate time  # noqa: E501

        :return: The calculate_time of this UnifiedPortfolioOutput.  # noqa: E501
        :rtype: int
        """
        return self._calculate_time

    @calculate_time.setter
    def calculate_time(self, calculate_time):
        """Sets the calculate_time of this UnifiedPortfolioOutput.

        Calculate time  # noqa: E501

        :param calculate_time: The calculate_time of this UnifiedPortfolioOutput.  # noqa: E501
        :type: int
        """

        self._calculate_time = calculate_time

    @property
    def risk_unit(self):
        """Gets the risk_unit of this UnifiedPortfolioOutput.  # noqa: E501

        Risk unit  # noqa: E501

        :return: The risk_unit of this UnifiedPortfolioOutput.  # noqa: E501
        :rtype: list[MockRiskUnit]
        """
        return self._risk_unit

    @risk_unit.setter
    def risk_unit(self, risk_unit):
        """Sets the risk_unit of this UnifiedPortfolioOutput.

        Risk unit  # noqa: E501

        :param risk_unit: The risk_unit of this UnifiedPortfolioOutput.  # noqa: E501
        :type: list[MockRiskUnit]
        """

        self._risk_unit = risk_unit

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
        if not isinstance(other, UnifiedPortfolioOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UnifiedPortfolioOutput):
            return True

        return self.to_dict() != other.to_dict()
