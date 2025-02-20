import bitget.bitget_api as baseApi
import bitget.consts as bg_constants

from bitget.exceptions import BitgetAPIException

if __name__ == '__main__':
    apiKey = "bg_0fcc6babcd593ec94288b99a7445e196"
    secretKey = "8e715cf50188997531fa00c9e607f201a70e394b920e1986163e6e453475d10c"
    passphrase = "robin3910"
    baseApi = baseApi.BitgetApi(apiKey, secretKey, passphrase)

    # Demo 获取品种精度
    try:
        params = {}
        params["symbol"] = "BTCUSDT"
        params["productType"] = "USDT-FUTURES"
        response = baseApi.get("/api/v2/mix/market/contracts", params)
        print(response)
    except BitgetAPIException as e:
        print("error:" + e.message)


    # Demo 平仓
    # try:
    #     params = {}
    #     params["symbol"] = "BTCUSDT"
    #     params["productType"] = "susdt-futures"
    #     # params["holdSide"] = "long"
    #     response = baseApi.post("/api/v2/mix/order/close-positions", params)
    #     print(response)
    # except BitgetAPIException as e:
    #     print("error:" + e.message)


    # Demo 获取仓位信息
    # {'code': '00000', 'msg': 'success', 'requestTime': 1739621779055, 'data': [{'marginCoin': 'USDT', 'symbol': 'BTCUSDT', 'holdSide': 'long', 'openDelegateSize': '0.01', 'marginSize': '96.0616', 'available': '0.01', 'locked': '0', 'total': '0.01', 'leverage': '10', 'achievedProfits': '0', 'openPriceAvg': '96061.6', 'marginMode': 'crossed', 'posMode': 'one_way_mode', 'unrealizedPL': '14.338', 'liquidationPrice': '-9880613.7641839999', 'keepMarginRate': '0.004', 'markPrice': '97495.4', 'marginRatio': '0.000087489769', 'breakEvenPrice': '96208.214834900941', 'totalFee': '-0.31252946', 'deductedFee': '0.5763696', 'grant': '', 'assetMode': 'single', 'autoMargin': 'off', 'takeProfit': None, 'stopLoss': None, 'takeProfitId': None, 'stopLossId': None, 'cTime': '1739431888793', 'uTime': '1739621073343'}]} 
    # try:
    #     params = {}
    #     params["symbol"] = "BTCUSDT"
    #     params["productType"] = "SUSDT-FUTURES"
    #     params["marginCoin"] = "USDT"
    #     response = baseApi.get("/api/v2/mix/position/single-position", params)
    #     print(response)
    # except BitgetAPIException as e:
    #     print("error:" + e.message)


    # Demo 批量获取挂单信息
    # api/v2/mix/order/orders-pending
    # try:
    #     params = {}
    #     params["productType"] = "SUSDT-FUTURES"
    #     response = baseApi.get("/api/v2/mix/order/orders-pending", params)
    #     print(response)
    # except BitgetAPIException as e:
    #     print("error:" + e.message)

    # Demo 取消挂单
    #  /api/v2/mix/order/cancel-order
    # try:
    #     params = {}
    #     params['symbol'] = "BTCUSDT"
    #     params["productType"] = "SUSDT-FUTURES"
    #     params['orderId'] = "1234567890"
    #     response = baseApi.post("/api/v2/mix/order/cancel-order", params)
    #     print(response)
    # except BitgetAPIException as e:
    #     print("error:" + e.message)

    # 撤销所有挂单
    # try:
    #     params = {}
    #     params["symbol"] = "SBTCSUSDT"
    #     params["productType"] = "SUSDT-FUTURES"
    #     response = baseApi.post("/api/v2/mix/order/cancel-all-orders", params)
    #     print(response)
    # except BitgetAPIException as e:
    #     print("error:" + e.message)
