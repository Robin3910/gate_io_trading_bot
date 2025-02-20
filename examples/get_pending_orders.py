import bitget.bitget_api as baseApi
import bitget.consts as bg_constants

from bitget.exceptions import BitgetAPIException

if __name__ == '__main__':
    apiKey = "bg_0fcc6babcd593ec94288b99a7445e196"
    secretKey = "8e715cf50188997531fa00c9e607f201a70e394b920e1986163e6e453475d10c"
    passphrase = "robin3910"
    baseApi = baseApi.BitgetApi(apiKey, secretKey, passphrase)


    # Demo 批量获取挂单信息
    # api/v2/mix/order/orders-pending
    try:
        params = {}
        params["productType"] = "usdt-futures"
        response = baseApi.get("/api/v2/mix/order/orders-pending", params)
        print(response)
    except BitgetAPIException as e:
        print("error:" + e.message)
