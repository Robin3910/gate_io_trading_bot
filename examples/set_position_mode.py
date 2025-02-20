import bitget.bitget_api as baseApi
import bitget.consts as bg_constants

from bitget.exceptions import BitgetAPIException

if __name__ == '__main__':
    apiKey = "bg_0fcc6babcd593ec94288b99a7445e196"
    secretKey = "8e715cf50188997531fa00c9e607f201a70e394b920e1986163e6e453475d10c"
    passphrase = "robin3910"
    baseApi = baseApi.BitgetApi(apiKey, secretKey, passphrase)


    # 调整持仓模式 为 单向持仓
    try:
        params = {}
        params["posMode"] = "one_way_mode"
        params["productType"] = "USDT-FUTURES"
        response = baseApi.post("/api/v2/mix/account/set-position-mode", params)
        print(response)
    except BitgetAPIException as e:
        print("error:" + e.message)
