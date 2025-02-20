# Base Url
API_URL = 'https://api.bitget.com'
CONTRACT_WS_URL = 'wss://ws.bitget.com/mix/v1/stream'
# 测试环境为test，生产环境为prd
ENV = 'test'
PRODUCT_TYPE = 'SUSDT-FUTURES' if ENV == 'test' else 'USDT-FUTURES'

# http header
CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'ACCESS-KEY'
OK_ACCESS_SIGN = 'ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'

# header key
LOCALE = 'locale'

# method
GET = "GET"
POST = "POST"
DELETE = "DELETE"

# sign type
RSA = "RSA"
SHA256 = "SHA256"
SIGN_TYPE = SHA256

# ws
REQUEST_PATH = '/user/verify'

# ACCOUNT INFO
API_KEY = '6953af36dcec691ee0cb266cf60d13e58bcc3f9c8f9d71b8b899090e649e3898'
API_SECRET = '2e9d0e67d0585312bbefc7aa7e4dcbdb1d2991b8b7665a76c4c11b022bc88f91'
API_PASSPHRASE = 'robin3910'
IP_WHITE_LIST = ['52.89.214.238', '34.212.75.30', '54.218.53.128', '52.32.178.7', '127.0.0.1']

# 微信通知配置
WX_TOKEN = 'SCT264877TGGj2xxxF6g'


# 错误码
SUCCESS = "00000"
