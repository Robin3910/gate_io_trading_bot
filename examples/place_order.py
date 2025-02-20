# !/usr/bin/env python
# coding: utf-8

from decimal import Decimal as D, ROUND_UP, getcontext

from gate_api import ApiClient, Configuration, FuturesApi, FuturesOrder, Transfer, WalletApi
from gate_api.exceptions import GateApiException

from config import RunConfig

SETTLE = "usdt"

def place_order(symbol, side, qty, price, order_type="limit"):
    """下单"""
    if order_type == "limit":
        tif = "gtc"
        if price == 0:
            raise ValueError("price must be greater than 0 for limit order")
    else:
        tif = "ioc"
        price = 0
    

    if side == "sell":
        qty = -qty
        
    order = FuturesOrder(contract=symbol, size=qty, price=price, tif=tif)
    try:
        order_response = futures_api.create_futures_order(SETTLE, order)
        print("order %s created with status: %s", order_response.id, order_response.status)
        return order_response.id
    except GateApiException as ex:
        print("error encountered creating futures order: %s", ex)
        return

if __name__ == '__main__':
    gate_config = Configuration(key="baffffe996db428683cc4c9ea945ad87", secret="a9e3f7eb91f9b545ca8d690fe93a99fcb709445a68f21cbfd83fae91f4510288", host="https://fx-api-testnet.gateio.ws/api/v4")
    futures_api = FuturesApi(ApiClient(gate_config))
    settle = SETTLE
    symbol = "BTC_USDT"
    try:
        order_response = place_order(symbol, "buy", 2, 93000)
        print(order_response)
    except GateApiException as ex:
        print("error encountered creating futures order: %s", ex)
