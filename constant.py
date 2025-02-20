# Base Url
CONTRACT_WS_URL = 'wss://fx-api-testnet.gateio.ws/v4/ws'
# 测试环境为test，生产环境为prd
ENV = 'test'
API_URL = 'https://api.gateio.ws/api/v4' if ENV == 'prd' else 'https://fx-api-testnet.gateio.ws/api/v4'

PRODUCT_TYPE = 'USDT-FUTURES'

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
API_KEY = 'baffffe996db428683cc4c9ea945ad87'
API_SECRET = 'a9e3f7eb91f9b545ca8d690fe93a99fcb709445a68f21cbfd83fae91f4510288'
API_PASSPHRASE = 'robin3910'
IP_WHITE_LIST = ['52.89.214.238', '34.212.75.30', '54.218.53.128', '52.32.178.7', '127.0.0.1']

# 微信通知配置
WX_TOKEN = 'SCT264877TGGj2xxxF6g'
SETTLE = 'usdt'

# 错误码
SUCCESS = "00000"
