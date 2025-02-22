# Gate.io Trading Bot

这是一个基于Gate.io交易所API的自动化交易机器人，支持期货交易，具有网页管理界面。
接收tradingview信号并进行对应的逻辑处理

## 主要功能

- 支持多币种同时交易
- 支持做多/做空策略
- 支持区间交易
- 支持移动止盈
- 支持分批止盈
- 支持亏损后自动降低仓位
- 支持Web界面配置和监控
- 支持微信消息通知

## 系统要求

- Python 3.x
- Flask
- Gate.io API Key和Secret
- 服务器或本地运行环境

## 安装步骤

1. 克隆代码库

```bash
git clone https://github.com/yourusername/gateio-trading-bot.git
cd gateio-trading-bot
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建`constant.py`文件并设置以下参数：
```python
WX_TOKEN = "your_weixin_token"  # 微信通知token
SETTLE = "usdt"  # 结算币种
IP_WHITE_LIST = ["127.0.0.1"]  # IP白名单
```

## 使用说明

1. 启动服务
```bash
nohup python trading_bot.py &
```

2. 访问Web界面
- 打开浏览器访问 `http://{your_server_ip}:80`

3. 配置交易参数
```json
{
  "symbol": "BTCUSDT",          // 交易币种
  "total_usdt": 10000,          // 总保证金
  "every_zone_usdt": 0.02,      // 每个区间投入的资金比例
  "loss_decrease": 0.25,        // 亏损后降低仓位比例
  "direction": "buy/sell",      // 交易方向
  "entry_config": "",           // 入场配置
  "exit_config": "",            // 出场配置
  "pos_for_trail": "",          // 移动止盈预留仓位
  "trail_active_price": 0.6,    // 移动止盈触发点
  "trail_callback": 0.1,        // 移动止盈回调比例
  "up_line": 0,                 // 上轨价格
  "down_line": 0                // 下轨价格
}
```

## 功能特点

1. 区间交易
- 支持自定义上下轨
- 支持分批入场和出场
- 支持自动调整仓位

2. 风险控制
- 支持止损设置
- 支持移动止盈
- 支持亏损后自动降低仓位

3. 监控功能
- Web界面实时监控
- 微信消息通知
- 交易日志记录

## 注意事项

1. 请确保API权限设置正确
2. 建议先在测试网进行测试
3. 请合理设置交易参数
4. 建议设置IP白名单增加安全性

## 许可证

MIT License

## 免责声明

本项目仅供学习和研究使用，作者不对使用本项目造成的任何损失负责。在使用本项目进行实盘交易前，请充分了解风险。
