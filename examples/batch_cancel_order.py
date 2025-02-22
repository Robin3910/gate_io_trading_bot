# !/usr/bin/env python
# coding: utf-8

from decimal import Decimal as D, ROUND_UP, getcontext

from gate_api import ApiClient, Configuration, FuturesApi, FuturesOrder, Transfer, WalletApi
from gate_api.exceptions import GateApiException

from config import RunConfig

SETTLE = "usdt"


if __name__ == '__main__':
    gate_config = Configuration(key="baffffe996db428683cc4c9ea945ad87", secret="a9e3f7eb91f9b545ca8d690fe93a99fcb709445a68f21cbfd83fae91f4510288", host="https://fx-api-testnet.gateio.ws/api/v4")
    futures_api = FuturesApi(ApiClient(gate_config))
    settle = SETTLE
    symbol = "BTC_USDT"
    """批量撤销指定ID的挂单"""
    order_id_list = [
        "58828270150120222"
    ]
    try:
        order_response = futures_api.cancel_batch_future_orders(SETTLE, order_id_list)
        print(order_response)
    except GateApiException as ex:
        print(f'{symbol}|批量撤销挂单失败，错误: {ex}')
