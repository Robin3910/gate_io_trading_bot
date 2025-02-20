import bitget.bitget_api as baseApi
import bitget.consts as bg_constants

from bitget.exceptions import BitgetAPIException

if __name__ == '__main__':
    apiKey = "bg_0fcc6babcd593ec94288b99a7445e196"
    secretKey = "8e715cf50188997531fa00c9e607f201a70e394b920e1986163e6e453475d10c"
    passphrase = "robin3910"
    baseApi = baseApi.BitgetApi(apiKey, secretKey, passphrase)


    # Demo 取消挂单
    #  /api/v2/mix/order/cancel-order
    try:
        params = {}
        params['symbol'] = "BTCUSDT"
        params["productType"] = "SUSDT-FUTURES"
        params['orderId'] = "1234567890"
        response = baseApi.post("/api/v2/mix/order/cancel-order", params)
        print(response)
    except BitgetAPIException as e:
        print("error:" + e.message)

    # 撤销所有挂单
    # try:
    #     params = {}
    #     params["symbol"] = "SBTCSUSDT"
    #     params["productType"] = "SUSDT-FUTURES"
    #     response = baseApi.post("/api/v2/mix/order/cancel-all-orders", params)
    #     print(response)
    # except BitgetAPIException as e:
    #     print("error:" + e.message)
