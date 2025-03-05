# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from functools import wraps
import threading
import time
import requests
from datetime import datetime, timedelta
import json
import logging
from logging.handlers import RotatingFileHandler
import constant as CONFIG
from decimal import Decimal as D, ROUND_UP, getcontext
from gate_api import ApiClient, Configuration, FuturesApi, FuturesOrder, FuturesPriceTriggeredOrder,FuturesPriceTrigger,FuturesInitialOrder, Transfer, WalletApi
from gate_api.exceptions import GateApiException
import secrets

app = Flask(__name__)

# TODO 待办
# 1、测试一下monitor_price的逻辑 - done
# 2、需要补充一个页面，让用户可以配置API和secret，也可以手动停止策略的运行 - done
# 3、在页面中需要展示当前的策略参数，比如当前的仓位，当前的挂单，当前的止损单，当前的移动止盈单 - done
# 4、补充处理失败的时候，微信发出告警 -done
# 5、测试指标到服务器的逻辑 - done
# 6、待写逻辑：如果亏损了，下一次要减少开仓。如果盈利了，下次再恢复回来 - done
# 7、重置策略状态的时候，需要先暂停策略，再重置，再恢复策略 - done
# 8、补充一下价格触发类型订单
# 9、移动止盈仓位，在分批止盈之后就会被重新设置，需要修改一下，应该是设置好一次之后，不要重复去变化了，而是等待下一次入场单成交了，才能再去修改

# 配置信息
WX_TOKEN = CONFIG.WX_TOKEN
PRODUCT_TYPE = CONFIG.PRODUCT_TYPE
SETTLE = CONFIG.SETTLE
# 添加 Flask secret key
app.secret_key = secrets.token_hex(16)


ip_white_list = CONFIG.IP_WHITE_LIST
# baseApi = baseApi.BitgetApi(CONFIG.API_KEY, CONFIG.API_SECRET, CONFIG.API_PASSPHRASE)
gate_config = Configuration(key="baffffe996db428683cc4c9ea945ad87", secret="a9e3f7eb91f9b545ca8d690fe93a99fcb709445a68f21cbfd83fae91f4510288", host="https://fx-api-testnet.gateio.ws/api/v4")
futures_api = FuturesApi(ApiClient(gate_config))

paused = True # 全局总开关：是否暂停。开启后，就暂停所有策略的运行
is_logined = False # 是否登录

symbol_tick_size = {} # 币种精度

api_key = ""
api_secret = ""

# 对币种信息预处理
def prefix_symbol(s: str) -> str:
    # BINANCE:BTCUSDT.P -> BTC_USDT
    # 首先处理冒号，如果存在则取后面的部分
    if ':' in s:
        s = s.split(':')[1]
    
    # 检查字符串是否以".P"结尾并移除
    if s.endswith('.P'):
        s = s[:-2]

    # 将BTCUSDT转成BTC_USDT
    s = s.replace('USDT', '_USDT')

    return s

def send_wx_notification(title, message):
    """
    发送微信通知
    
    Args:
        title: 通知标题
        message: 通知内容
    """
    try:
        mydata = {
            'title': title,
            'desp': message
        }
        requests.post(f'https://sctapi.ftqq.com/{WX_TOKEN}.send', data=mydata)
        logger.info('发送微信消息成功')
    except Exception as e:
        logger.error(f'发送微信消息失败: {str(e)}')

def get_decimal_places(tick_size):
    tick_str = str(float(tick_size))
    if '.' in tick_str:
        return len(tick_str.split('.')[-1].rstrip('0'))
    return 0

# 配置日志
def setup_logger():
    logger = logging.getLogger('gate_bot')
    logger.setLevel(logging.INFO)
    
    # 创建 rotating file handler，最大文件大小为 10MB，保留 5 个备份文件
    handler = RotatingFileHandler('gate_bot.log', maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

logger = setup_logger()

def place_order(symbol, side, qty, price, order_type="limit", reduce_only=False):
    """下单"""
    # 带price就是委托单，不带price是市价单
    if order_type == "limit":
        tif = "gtc"
    else:
        tif = "ioc"
        price = 0
    

    if side == "sell":
        qty = -qty
        
    order = FuturesOrder(contract=symbol, size=qty, price=price, tif=tif, reduce_only=reduce_only)
    try:
        order_response = futures_api.create_futures_order(SETTLE, order)
        logger.info(f"order {order_response.id} created with status: {order_response.status}")
        return str(order_response.id)
    except GateApiException as ex:
        logger.error(f"error encountered creating futures order: {ex}")
        send_wx_notification(f"{symbol}|下单失败", f"下单失败: {ex}")
        return


def cancel_price_trigger_order(symbol):
    """取消价格触发单"""
    try:
        order_response = futures_api.cancel_price_triggered_order_list(SETTLE, contract=symbol)
        return order_response
    except GateApiException as ex:
        logger.error(f"error encountered canceling price trigger order: {ex}")
        send_wx_notification(f"{symbol}|取消价格触发单失败", f"取消价格触发单失败: {ex}")

def place_price_trigger_order(symbol, side, qty, price, order_type="limit", rule=1, reduce_only=False):
    """下单"""
    order_price = str(price)
    trigger_price = str(price)
    if order_type == "limit":
        tif = "gtc"
    else:
        tif = "ioc"
        order_price = "0"
    

    if side == "sell":
        qty = -qty
    
    # rule 1 代表价格 >= 触发价时触发， 2 代表价格 <= 触发价时触发
    initial_order = FuturesInitialOrder(contract=symbol, size=qty, price=order_price, tif=tif, reduce_only=reduce_only)
    trigger_order = FuturesPriceTrigger(strategy_type=0, price_type=0, price=trigger_price, rule=rule)
    order = FuturesPriceTriggeredOrder(initial=initial_order, trigger=trigger_order)
    try:
        order_response = futures_api.create_price_triggered_order(SETTLE, order)
        return str(order_response.id)
    except GateApiException as ex:
        logger.error(f"error encountered creating futures order: {ex}")
        send_wx_notification(f"{symbol}|挂单失败", f"挂单失败: {ex}")
        return

def query_order(symbol, order_id):
    """查询订单"""
    try:
        order_response = futures_api.get_futures_order(SETTLE, order_id)
        return order_response
    except GateApiException as ex:
        logger.error(f'{symbol}|查询订单失败，错误: {ex}')
        return None

def close_position(symbol):
    """市价平仓"""
    order = FuturesOrder(contract=symbol, size="0", close="true", price="0", tif="ioc")
    try:
        order_response = futures_api.create_futures_order(SETTLE, order)
        return order_response.id
    except GateApiException as ex:
        if ex.label == "POSITION_EMPTY":
            return None
        else:
            logger.error(f'{symbol}|平仓失败，错误: {ex}')
            send_wx_notification(f"{symbol}|平仓失败", f"平仓失败: {ex}")
            return None

def get_position(symbol):
    """获取仓位"""
    position_size = 0
    try:
        position = futures_api.get_position(SETTLE, symbol)
        position_size = position.size
        return position_size
    except GateApiException as ex:
        logger.error(f'{symbol}|获取仓位失败，错误: {ex}')
        return 0

def batch_place_order(symbol, order_list, reduce_only=False):
    """批量下单"""
    try:
        place_order_list = []
        for order in order_list:
            qty = order['size']
            tif = "gtc"
            price = order['price']
            # 带price就是委托单，不带price是市价单
            if order['orderType'] == "limit":
                tif = "gtc"
            else:
                tif = "ioc"
                price = 0
            
            if order['side'] == "sell":
                qty = -qty
                
            order = FuturesOrder(contract=symbol, size=qty, price=price, tif=tif, reduce_only=reduce_only)
            place_order_list.append(order)
        order_response = futures_api.create_batch_futures_order(SETTLE, place_order_list)
        return order_response
    except GateApiException as ex:
        logger.error(f'{symbol}|批量下单失败，错误: {ex}')
        send_wx_notification(f"{symbol}|批量下单失败", f"批量下单失败: {ex}")
        return None

def get_pending_orders(symbol):
    """获取挂单信息"""
    try:
        order_list = futures_api.list_futures_orders(SETTLE, status="open", contract=symbol)
        return order_list
    except GateApiException as ex:
        logger.error(f'{symbol}|获取挂单信息失败，错误: {ex}')
        return None

def cancel_order(symbol, order_id):
    """取消指定ID的挂单"""
    try:
        order_response = futures_api.cancel_futures_order(SETTLE, order_id)
        logger.info(f'{symbol}|取消挂单成功: {order_response}')
    except GateApiException as ex:
        logger.error(f'{symbol}|取消挂单失败，错误: {ex}')
        send_wx_notification(f"{symbol}|取消挂单失败", f"取消挂单失败: {ex}")

def cancel_all_orders(symbol):
    """取消该品种所有的挂单"""
    try:
        pending_orders = futures_api.list_futures_orders(SETTLE, status="open", contract=symbol)
        if pending_orders:
            order_id_list = [str(order.id) for order in pending_orders]
            order_response = futures_api.cancel_batch_future_orders(SETTLE, order_id_list)
            logger.info(f'{symbol}|取消挂单成功: {order_response}')
        else:
            logger.info(f'{symbol}|没有挂单')

        # 取消价格触发单
        cancel_price_trigger_order(symbol)
    except GateApiException as ex:
        logger.error(f'{symbol}|取消挂单失败，错误: {ex}')
        send_wx_notification(f"{symbol}|取消所有挂单失败", f"取消挂单失败: {ex}")

def set_leverage(symbol, leverage):
    """设置杠杆"""
    try:
        futures_api.update_position_leverage(SETTLE, symbol, leverage=0, cross_leverage_limit=leverage)
    except GateApiException as ex:
        logger.error(f'{symbol}|设置杠杆失败，错误: {ex}')
        return None

def set_position_mode(is_dual_mode):
    """设置持仓模式"""
    # is_dual_mode 为True表示双向持仓，为False表示单向持仓
    try:
        dual_mode_response = futures_api.set_dual_mode(SETTLE, is_dual_mode)
        return dual_mode_response
    except GateApiException as ex:
        logger.error(f'设置持仓模式失败，错误: {ex}')
        return None

def batch_cancel_orders(symbol, order_id_list):
    """批量撤销指定ID的挂单"""
    try:
        order_response = futures_api.cancel_batch_future_orders(SETTLE, order_id_list)
        return order_response
    except GateApiException as ex:
        logger.error(f'{symbol}|批量撤销挂单失败，错误: {ex}')
        send_wx_notification(f"{symbol}|批量撤销挂单失败", f"批量撤销挂单失败: {ex}")
        return None

def get_single_contract(symbol):
    """获取单个合约信息"""
    try:
        order_response = futures_api.get_futures_contract(SETTLE, symbol)
        return order_response
    except GateApiException as ex:
        logger.error(f'{symbol}|获取单个合约信息失败，错误: {ex}')
        return None
    
def get_mark_price(symbol):
    """获取标记价格"""
    try:
        order_response = futures_api.get_futures_contract(SETTLE, symbol)
        return float(order_response.mark_price)
    except GateApiException as ex:
        logger.error(f'{symbol}|获取标记价格失败，错误: {ex}')
        return None

# 设置持仓模式
# set_position_mode(False)

# 获取币种的精度
def get_symbol_tick_size():
    try:
        global symbol_tick_size
        exchange_info = futures_api.list_futures_contracts(SETTLE)
        for item in exchange_info:
            symbol_tick_size[item.name] = {
                'tick_size': len(str(float(item.order_price_round)).split('.')[-1].rstrip('0')),
                'min_qty': len(str(float(item.order_size_min)).split('.')[-1].rstrip('0')),
                "qty_to_contract": float(item.quanto_multiplier),
                "order_price_round": float(item.order_price_round)
            }

            # if item.name == "BNB_USDT":
            #     print(item)
            #     print(symbol_tick_size[item.name])
        logger.info(f'获取币种精度成功')
    except GateApiException as ex:
        logger.error(f'获取币种精度失败，错误: {ex}')

def amountConvertToContract(_symbol, _amount):
    """将数量转换为张数"""
    global symbol_tick_size
    qty_to_contract = symbol_tick_size[_symbol]['qty_to_contract']
    return int(_amount / qty_to_contract)

def round_to_step(price, step, decimal_places):
    """将价格四舍五入到最小步长的倍数"""
    # 将价格除以步长，四舍五入到整数，然后再乘以步长
    rounded = round(price / step) * step
    # 保留指定小数位
    return round(rounded, decimal_places)

# 创建全局字典来存储不同币种的交易信息
trading_pairs = {}

class GridTrader:
    def __init__(self, symbol):
        self.symbol = symbol
        self.total_usdt = 0
        self.every_zone_usdt = 0 # 百分比
        self.zone_usdt = 0 # 预期一个区间要投入的金额
        self.loss_decrease = 0
        self.current_loss_decrease = 0
        self.direction = ""
        self.entry_config = ""
        self.exit_config = ""
        self.pos_for_trail = 0
        self.trail_active_percent = 0
        self.trail_active_price = 0
        self.trail_callback = 0
        self.up_line = 0
        self.down_line = 0
        self.entry_list = []
        self.exit_list = []
        self.monitor_thread = None # 监控线程
        self.loss_count = 0 # 亏损次数
        self.trail_high_price = 0 # 移动止盈的最高价格
        self.trail_low_price = 999999 # 移动止盈的最低价格
        self.stop_loss_order_id = None # 止损单ID
        self.position = 0 # 持仓数量
        self.mark_price = 0 # 标记价格
        self.is_handling = False # 是否正在处理
        self.threshold_position_for_update = 0 # 更新出场单的仓位阈值，只有>=这个仓位的时候，才会去更新出场单
        self.pre_position = 0 # 监控中的上一个仓位值大小
        self.zone_usdt = 0 # 预期一个区间要投入的金额
        self.finished = False # 区间的逻辑是否完成了
        self.paused = True # 该品种是否暂停
        
        logger.info(f'{symbol} GridTrader 初始化完成')

    def is_need_update_trading_params(self, data):
        """判断是否需要更新交易参数"""
        if self.is_handling:
            return False
        if not is_logined:
            return False
        if paused:
            return False
        if self.paused:
            return False
        position = get_position(self.symbol)
        if position != 0:
            return False
        order_price_round = symbol_tick_size[self.symbol]['order_price_round']
        tick_size = symbol_tick_size[self.symbol]['tick_size']
        up_line = round_to_step(float(data['up_line']), order_price_round, tick_size)
        down_line = round_to_step(float(data['down_line']), order_price_round, tick_size)
        if data['direction'] != self.direction:
            # 反转的时候，需要更新交易参数
            return True
        elif data['direction'] == self.direction and position == 0 and (up_line != self.up_line or down_line != self.down_line):
            # 无仓位的时候，如果上下沿价格改变，则需要更新交易参数
            return True
        else:
            return False

    def update_trading_params(self, data):
        if self.is_need_update_trading_params(data):
            try:
                self.is_handling = True
                # 平仓
                close_position(self.symbol)
                # 取消所有挂单
                cancel_all_orders(self.symbol)
                # 设置一下杠杆，默认5倍杠杆
                set_leverage(self.symbol, 5)

                if symbol_tick_size[self.symbol] is None:
                    logger.error(f'{self.symbol} 精度不存在|重新获取精度')
                    contract_info = get_single_contract(self.symbol)
                    symbol_tick_size[self.symbol] = {
                        'tick_size': len(str(float(contract_info.order_price_round)).split('.')[-1].rstrip('0')),
                        'min_qty': len(str(float(contract_info.order_size_min)).split('.')[-1].rstrip('0')),
                        "qty_to_contract": float(contract_info.quanto_multiplier),
                        "order_price_round": float(contract_info.order_price_round)
                    }
                # 更新新的方向的参数
                logger.info(f'{self.symbol} |更新交易参数: {json.dumps(data, ensure_ascii=False)}')
                self.total_usdt = float(data['total_usdt'])
                self.every_zone_usdt = float(data['every_zone_usdt']) # 百分数
                self.loss_decrease = float(data['loss_decrease'])
                self.direction = data['direction']
                self.entry_config = data['entry_config']
                self.exit_config = data['exit_config']
                self.pos_for_trail = float(data['pos_for_trail'])
                self.trail_active_percent = float(data['trail_active_price']) # 移动止盈的触发percent
                self.trail_callback = float(data['trail_callback'])
                self.up_line = round_to_step(float(data['up_line']), symbol_tick_size[self.symbol]['order_price_round'], symbol_tick_size[self.symbol]['tick_size'])
                self.down_line = round_to_step(float(data['down_line']), symbol_tick_size[self.symbol]['order_price_round'], symbol_tick_size[self.symbol]['tick_size'])
                self.zone_usdt = self.total_usdt * self.every_zone_usdt # 预期一个区间要投入的金额
                if self.current_loss_decrease > 0:
                    self.zone_usdt = self.zone_usdt * (1 - self.current_loss_decrease)
                self.trail_high_price = 0 # 移动止盈的最高价格
                self.trail_low_price = 999999 # 移动止盈的最低价格
                self.stop_loss_order_id = None # 止损单ID
                self.threshold_position_for_update = 0 # 更新出场单的仓位阈值，只有>=这个仓位的时候，才会去更新出场单
                self.finished = False # 区间的逻辑是否完成了
                if self.direction == "buy":
                    # ------ 上沿 up_line 100000
                    #  ^
                    #  |
                    #  |
                    # ------ 下沿 down_line 90000
                    self.interval = round(self.up_line - self.down_line, symbol_tick_size[self.symbol]['tick_size'])
                    self.trail_active_price = round(self.down_line + self.interval * self.trail_active_percent, symbol_tick_size[self.symbol]['tick_size'])
                    # 解析入场配置
                    self.entry_list = []
                    if self.entry_config:
                        entry_configs = self.entry_config.split('|')
                        for config in entry_configs:
                            price_ratio, percent = config.split('_')
                            # 入场价格 = 下轨 + 价格处于区间的百分比 * 区间宽度
                            entry_price = round_to_step(self.down_line + float(price_ratio) * 0.01 * self.interval, symbol_tick_size[self.symbol]['order_price_round'], symbol_tick_size[self.symbol]['tick_size'])
                            entry_percent = float(percent) * 0.01
                            entry_zone_usdt = self.zone_usdt * entry_percent
                            entry_qty = amountConvertToContract(self.symbol, entry_zone_usdt/entry_price)
                            self.entry_list.append({
                                'entry_price': entry_price, # 入场价格
                                'percent': entry_percent,  # 投入资金百分比
                                'zone_usdt': entry_zone_usdt, # 投入资金
                                "qty": entry_qty, # 投入数量
                                "order_id": None # 订单ID
                            })
                        logger.info(f'{self.symbol} |入场配置解析结果: {json.dumps(self.entry_list, ensure_ascii=False)}')
                    
                    # 解析出场配置
                    self.exit_list = []
                    if self.exit_config:
                        exit_configs = self.exit_config.split('|')
                        for config in exit_configs:
                            price_ratio, percent = config.split('_')
                            exit_price = round_to_step(self.down_line + float(price_ratio)*0.01 * self.interval, symbol_tick_size[self.symbol]['order_price_round'], symbol_tick_size[self.symbol]['tick_size'])
                            exit_percent = float(percent) * 0.01
                            self.exit_list.append({
                                'exit_price': exit_price, # 退出价格
                                'percent': exit_percent,  # 离场资金百分比
                                'order_id': None # 订单ID
                            })
                        logger.info(f'{self.symbol} |出场配置解析结果: {json.dumps(self.exit_list, ensure_ascii=False)}')

                    # 挂上限价单
                    order_list = []
                    for entry in self.entry_list:
                        order_list.append({
                            "side": "buy",
                            "price": entry['entry_price'],
                            "size": entry['qty'],
                            "orderType": "limit"
                        })
                    ret_list = batch_place_order(self.symbol, order_list)
                    for i in range(len(ret_list)):
                        self.entry_list[i]['order_id'] = str(ret_list[i].id)

                elif self.direction == "sell":
                    # 做空的时候，因为预期是要往下走的，所以down_line是区间上沿的价格, up_line是区间下沿的价格
                    # ------ 上沿 down_line 100000
                    #  |
                    #  |
                    #  v
                    # ------ 下沿 up_line 90000
                    self.interval = round(self.down_line - self.up_line, symbol_tick_size[self.symbol]['tick_size'])
                    self.trail_active_price = round(self.down_line - self.interval * self.trail_active_percent, symbol_tick_size[self.symbol]['tick_size'])
                    # 解析入场配置
                    self.entry_list = []
                    if self.entry_config:
                        entry_configs = self.entry_config.split('|')
                        for config in entry_configs:
                            price_ratio, percent = config.split('_')
                            # 入场价格 = 下轨 - 价格处于区间的百分比 * 区间宽度
                            # 做空时下轨是区间上沿的价格
                            entry_price = round_to_step(self.down_line - (1 - float(price_ratio) * 0.01) * self.interval, symbol_tick_size[self.symbol]['order_price_round'], symbol_tick_size[self.symbol]['tick_size'])
                            entry_percent = float(percent) * 0.01
                            entry_zone_usdt = self.zone_usdt * entry_percent
                            entry_qty = amountConvertToContract(self.symbol, entry_zone_usdt/entry_price)
                            self.entry_list.append({
                                'entry_price': entry_price, # 入场价格
                                'percent': entry_percent,  # 投入资金百分比
                                'zone_usdt': entry_zone_usdt, # 投入资金
                                "qty": entry_qty, # 投入数量
                                "order_id": None # 订单ID
                            })
                        logger.info(f'{self.symbol} |入场配置解析结果: {json.dumps(self.entry_list, ensure_ascii=False)}')
                    
                    # 解析出场配置
                    self.exit_list = []
                    if self.exit_config:
                        exit_configs = self.exit_config.split('|')
                        for config in exit_configs:
                            price_ratio, percent = config.split('_')
                            exit_price = round_to_step(self.down_line - (float(price_ratio) * 0.01) * self.interval, symbol_tick_size[self.symbol]['order_price_round'], symbol_tick_size[self.symbol]['tick_size'])
                            exit_percent = float(percent) * 0.01
                            self.exit_list.append({
                                'exit_price': exit_price, # 退出价格
                                'percent': exit_percent,  # 离场资金百分比
                                'order_id': None # 订单ID
                            })
                        logger.info(f'{self.symbol} |出场配置解析结果: {json.dumps(self.exit_list, ensure_ascii=False)}')

                    # 挂限价单
                    order_list = []
                    for entry in self.entry_list:
                        order_list.append({
                            "side": "sell",
                            "price": entry['entry_price'],
                            "size": entry['qty'],
                            "orderType": "limit"
                        })
                    ret_list = batch_place_order(self.symbol, order_list)
                    for i in range(len(ret_list)):
                        self.entry_list[i]['order_id'] = str(ret_list[i].id)

                # 开启一个新的线程来监控成交情况
                if self.monitor_thread is None:
                    self.monitor_thread = threading.Thread(target=self.monitor_price)
                    self.monitor_thread.start()
                self.is_handling = False
                logger.info(f'{self.symbol} 更新交易参数成功|开始监控新的区间逻辑 {json.dumps(data, ensure_ascii=False)}')
            except Exception as e:
                logger.error(f'{self.symbol} 更新交易参数时发生错误: {str(e)}|数据：{json.dumps(data, ensure_ascii=False)}')
                self.is_handling = False
                send_wx_notification(f'{self.symbol} 更新交易参数时发生错误: {str(e)}', f'{self.symbol} 更新交易参数时发生错误: {str(e)}|数据：{json.dumps(data, ensure_ascii=False)}')
                return None

    def monitor_price(self):
        global paused, is_logined
        """监控价格并更新止损"""
        self.is_monitoring = True
        logger.info(f'{self.symbol} 开始价格监控')
        
        while True:
            if self.is_handling:
                # 如果发现当前正在处理，就先等待
                time.sleep(3)
                continue
            if not is_logined:
                paused = True
                time.sleep(3)
                continue
            if paused:
                time.sleep(3)
                continue
            if self.finished:
                time.sleep(3)
                continue
            if self.paused:
                # 当前品种暂停
                time.sleep(3)
                continue
            try:
                # 获取当前仓位和持仓方向
                position = get_position(self.symbol)
                self.pre_position = self.position # 记录上一次的仓位值
                self.position = position if self.direction == "buy" else -position # 更新当前仓位值
                # 获取当前所有挂单
                pending_orders = get_pending_orders(self.symbol)
                
                # 检查入场单状态
                # 无论有无仓位，都需要检查入场单所有的仓位以及当前持仓加起来是否等于预期要投入的值
                # 如果不足，则需要补单
                # 如果相等，则无需额外操作
                
                # 计算所有入场单、出场单的总数量
                total_entry_size = 0
                total_exit_size = 0
                entry_orders = []
                exit_orders = []
                if pending_orders:
                    for order in pending_orders:
                        # 检查是否是当前symbol的订单
                        if order.contract == self.symbol:
                            # 如果是做多，只统计买单;如果是做空，只统计卖单
                            if (self.direction == "buy" and float(order.size) > 0) or \
                               (self.direction == "sell" and float(order.size) < 0):
                                total_entry_size += abs(float(order.size))
                                entry_orders.append(str(order.id))
                            else:
                                total_exit_size += abs(float(order.size))
                                exit_orders.append(str(order.id))
                # logger.info(f'{self.symbol} 当前入场挂单总数量: {total_entry_size}')

                # 计算预期需要入场的总数量
                expected_entry_size = 0
                for entry in self.entry_list:
                    expected_entry_size += entry['qty']
                # logger.info(f'{self.symbol} 预期入场总数量: {expected_entry_size}')

                # 需要补入场单
                if total_entry_size + self.position < expected_entry_size:
                    logger.info(f'{self.symbol} 需要补入场单|预期入场数量：{expected_entry_size}|当前挂单+持仓：{total_entry_size+self.position}')
                    # 取消所有现有的入场挂单
                    if entry_orders:
                        batch_cancel_orders(self.symbol, entry_orders)
                    
                    # 重新计算并设置入场单
                    new_entry_orders = []
                    remaining_position = position  # 当前持仓量
                    
                    for entry in self.entry_list:  # 直接遍历原始列表
                        if remaining_position >= entry['qty']:
                            # 如果剩余持仓大于等于该入场点应有的持仓量，不需要在此价位补单
                            remaining_position -= entry['qty']
                        else:
                            # 需要补单的数量 = 应有持仓量 - 剩余持仓量
                            need_qty = entry['qty'] - remaining_position
                            if need_qty > 0:
                                new_entry_orders.append({
                                    "side": self.direction,
                                    "price": entry['entry_price'],
                                    "size": round(need_qty, symbol_tick_size[self.symbol]['min_qty']),
                                    "orderType": "limit"
                                })
                            remaining_position = 0
                    
                    # 批量下新的入场单
                    if new_entry_orders:
                        ret_list = batch_place_order(self.symbol, new_entry_orders)
                        # 更新入场单ID
                        for i, ret in enumerate(ret_list):
                            self.entry_list[i]['order_id'] = ret.id
                        logger.info(f'{self.symbol} 重新设置入场单成功: {json.dumps(new_entry_orders, ensure_ascii=False)}')
               
                # 有仓位，没有出场单，就得把出场单补上
                # 先检查已有仓位和入场单的挂单是否匹配
                # 如果匹配则无需处理

                # 更新出场单阈值（threshold_position_for_update）的逻辑介绍：
                # 1、由于每次出场之后，还会保留一部分移动止盈的仓位，所以这部分移动止盈的仓位就又会被划分成多个分批止盈以及移动止盈
                # 2、所以在第一次持有仓位的时候，记录仓位的值，如果后续的仓位一直没超过这个阈值，那无需更新出场单，维持第一次挂单的出场单
                # 3、如果仓位超过这个阈值，则需要更新出场单，因为可能入场单又进场了，仓位更多，需要分配多余的仓位到各个分批止盈点上，以及加大移动止盈的数量
                # 4、只在仓位发生变化的时候才去更新，防止反复刷新
                if self.position > 0 and self.position >= self.threshold_position_for_update and self.pre_position != self.position:
                    self.threshold_position_for_update = self.position
                    # 检查出场单是否足量
                    expacted_exit_qty = round(self.position * (1 - self.pos_for_trail), symbol_tick_size[self.symbol]['min_qty'])
                    if abs(total_exit_size - expacted_exit_qty) / expacted_exit_qty <= 0.02:
                        pass
                    else:
                        logger.info(f'{self.symbol} 需要补齐出场单|预期出场数量：{expacted_exit_qty}|当前挂单出场数量：{total_exit_size}')
                        # 需要补单
                        # 取消所有现有的出场挂单
                        if exit_orders:
                            batch_cancel_orders(self.symbol, exit_orders)
                            cancel_price_trigger_order(self.symbol)
                            # 创建新的出场订单
                        new_exit_orders = []
                        for exit_conf in self.exit_list:
                            # 用分批止盈的仓位来设计出场单
                            # 会预留一部分仓位来做移动止盈
                            exit_qty = round(self.position * (1 - self.pos_for_trail) * exit_conf['percent'], symbol_tick_size[self.symbol]['min_qty'])
                            if exit_qty > 0:
                                new_exit_orders.append({
                                    "side": "sell" if self.direction == "buy" else "buy",
                                    "price": exit_conf['exit_price'],
                                    "size": round(exit_qty, symbol_tick_size[self.symbol]['min_qty']),
                                    "orderType": "limit"
                                })
                        # 挂价格触发止损单
                        place_price_trigger_order(symbol=self.symbol, side="sell" if self.direction == "buy" else "buy", qty=self.position, price=self.down_line, order_type="market", rule=2 if self.direction == "buy" else 1, reduce_only=True)
                        if new_exit_orders:
                            ret_list = batch_place_order(self.symbol, new_exit_orders, True)
                            for i in range(len(ret_list)):
                                self.exit_list[i]['order_id'] = str(ret_list[i].id)

                # 检测当前价格是否已经达到了移动止盈的触发点以及止损点
                mark_price = get_mark_price(self.symbol)
                if mark_price:
                    mark_price = float(mark_price)
                    self.mark_price = mark_price
                    is_profit = 0 # 0表示未平仓，-1表示亏损，1表示盈利
                    if self.direction == "buy":
                        if mark_price < self.down_line:
                            close_position(self.symbol)
                            cancel_all_orders(self.symbol)
                            logger.info(f"{self.symbol}|做多|当前价格已经达到了止损点: {mark_price}")
                            send_wx_notification(f"{self.symbol}|做多|当前价格已经达到了止损点: {mark_price}", f"{self.symbol}|做多|当前价格已经达到了止损点: {mark_price}")
                            is_profit = -1
                            self.finished = True
                        if mark_price > self.trail_active_price:
                            # logger.info(f'{self.symbol} 当前价格已经达到了移动止盈的触发点: {mark_price}')
                            if mark_price > self.trail_high_price:
                                self.trail_high_price = mark_price
                        if (self.trail_high_price - mark_price) / mark_price > self.trail_callback:
                            logger.info(f"{self.symbol}|做多|当前价格从最高点回落超过{self.trail_callback}，平仓|区间逻辑结束")
                            # 平仓
                            close_position(self.symbol)
                            cancel_all_orders(self.symbol)
                            send_wx_notification(f"{self.symbol}|做多|当前价格从最高点回落超过{self.trail_callback}，平仓|区间逻辑结束", f"{self.symbol}|做多|当前价格从最高点回落超过{self.trail_callback}，平仓|区间逻辑结束")
                            is_profit = 1
                            self.finished = True
                    elif self.direction == "sell":
                        if mark_price > self.down_line:
                            close_position(self.symbol)
                            cancel_all_orders(self.symbol)
                            logger.info(f"{self.symbol}|做空|当前价格已经达到了止损点: {mark_price}")
                            send_wx_notification(f"{self.symbol}|做空|当前价格已经达到了止损点: {mark_price}", f"{self.symbol}|做空|当前价格已经达到了止损点: {mark_price}")
                            is_profit = -1
                            self.finished = True
                        if mark_price < self.trail_active_price:
                            # logger.info(f'{self.symbol} 当前价格已经达到了移动止盈的触发点: {mark_price}')
                            if mark_price < self.trail_low_price:
                                self.trail_low_price = mark_price
                        if (mark_price - self.trail_low_price) / self.trail_low_price > self.trail_callback:
                            logger.info(f"{self.symbol}|做空|当前价格从最低点回升超过{self.trail_callback}，平仓|区间逻辑结束")
                            # 平仓
                            close_position(self.symbol)
                            cancel_all_orders(self.symbol)
                            send_wx_notification(f"{self.symbol}|做空|当前价格从最低点回升超过{self.trail_callback}，平仓|区间逻辑结束", f"{self.symbol}|做空|当前价格从最低点回升超过{self.trail_callback}，平仓|区间逻辑结束")
                            is_profit = 1
                            self.finished = True
                    if is_profit != 0:
                        if is_profit > 0:
                            # 如果之前有降低仓位，则需要将仓位补上
                            if self.current_loss_decrease > 0:
                                self.current_loss_decrease -= self.loss_decrease
                                logger.info(f'{self.symbol} 盈利|恢复仓位|当前递减值：{self.current_loss_decrease}')
                            # 如果没有降低仓位，则无需操作
                            if self.current_loss_decrease == 0:
                                pass
                        if is_profit < 0:
                            # 如果产生亏损，则需要降低仓位
                            self.current_loss_decrease += self.loss_decrease
                            logger.info(f'{self.symbol} 产生亏损|降低仓位|当前递减值：{self.current_loss_decrease}')

                time.sleep(3)  # 每1秒检查一次
                
            except Exception as e:
                logger.error(f'{self.symbol} 监控价格时发生错误: {str(e)}')
                send_wx_notification(f'{self.symbol} 监控价格时发生错误: {str(e)}', f'{self.symbol} 监控价格时发生错误: {str(e)}')
                time.sleep(3)
                
    def stop_monitoring(self):
        """停止价格监控"""
        if self.monitor_thread:
            self.monitor_thread.join()
            logger.info(f'{self.symbol} 停止价格监控')


# {
#   "symbol": "BTCUSDT", // 币种
#   "total_usdt": 10000, // 总保证金
# 	"every_zone_usdt": 0.02, // 每次区间投入的金额
#   "loss_decrease": 0.25, // 每次区间亏损后，下一次需要降低多少比例的区间投入额
# 	"direction": "buy/sell", // 交易方向
#   "entry_config": "", // 入场配置
#   "exit_config": "", // 出场配置
#   "pos_for_trail": "", // 预留多少x%的仓位用于动态止盈
#   "trail_active_price": 0.6, // 当价格触达区间x%时，开始动态止盈
#   "trail_callback": 0.1, // 当价格从高点回落10%的时候，止盈出场
#   "up_line": 0, // 上轨
#   "down_line": 0, // 下轨
#   "api_key": "baffffe996db428683cc4c9ea945ad87", // 交易所API key
#   "api_secret": "a9e3f7eb91f9b545ca8d690fe93a99fcb709445a68f21cbfd83fae91f4510288", // 交易所API secret
#   "env": "TEST/PRD", // 环境
# }
# 
@app.route('/message', methods=['POST'])
def handle_message():
    try:
        if not is_logined:
            return jsonify({"status": "error", "message": "未登录"})

        data = request.get_json()
        # global api_key, api_secret, is_logined, futures_api
        # if not is_logined or api_key != data['api_key'] or api_secret != data['api_secret']:
        #     if data['api_key'] and data['api_secret']:
        #         api_key = data['api_key']
        #         api_secret = data['api_secret']
        #         environment = data['env'].upper()
        #         host = "https://fx-api-testnet.gateio.ws/api/v4" if environment == 'TEST' else "https://fx-api.gateio.ws/api/v4"
        #         gate_config = Configuration(key=api_key, secret=api_secret, host=host)
        #         futures_api = FuturesApi(ApiClient(gate_config))
        #         account_res = futures_api.list_futures_accounts(SETTLE)
        #         if account_res:
        #             get_symbol_tick_size()
        #             is_logined = True
        #             logger.info(f'登录成功')
        #     else:
        #         return jsonify({"status": "error", "message": "API key 或 secret 不能为空"})
            
        symbol = prefix_symbol(data['symbol'])
        logger.info(f'收到 {symbol} 的新交易参数请求: {json.dumps(data, ensure_ascii=False)}')
        
        if symbol not in trading_pairs:
            # 创建或更新 GridTrader 实例
            trading_pairs[symbol] = GridTrader(symbol)
        
        # 设置交易参数
        trading_pairs[symbol].update_trading_params(data)
        
        # logger.info(f'{symbol} 交易参数设置成功')
        return jsonify({"status": "success", "message": f"{symbol} 接收消息成功"})
    except Exception as e:
        logger.error(f'设置交易参数失败: {str(e)}')
        return jsonify({"status": "error", "message": str(e)})

# @app.before_request
# def before_req():
#     logger.info(request.json)
#     if request.json is None:
#         return jsonify({'error': '请求体不能为空'}), 400
#     if request.remote_addr not in ip_white_list:
#         logger.info(f'ipWhiteList: {ip_white_list}')
#         logger.info(f'ip is not in ipWhiteList: {request.remote_addr}')
#         return jsonify({'error': 'ip is not in ipWhiteList'}), 403

@app.before_request
def before_req():
    # 排除登录路由和静态文件
    if request.path == '/login' or request.path == '/' or request.path.startswith('/static'):
        return
        
    # 只对 POST 请求进行 JSON 和 IP 检查
    if request.method == 'POST':
        # 检查 Content-Type
        if not request.is_json:
            return jsonify({'error': 'Content-Type 必须是 application/json'}), 415
            
        if request.json is None:
            return jsonify({'error': '请求体不能为空'}), 400
            
        if request.path != '/update_config' and request.remote_addr not in ip_white_list:
            logger.info(f'ipWhiteList: {ip_white_list}')
            logger.info(f'ip is not in ipWhiteList: {request.remote_addr}')
            return jsonify({'error': 'ip is not in ipWhiteList'}), 403

# 添加登录验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 登录路由
@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'andy123':
            session['logged_in'] = True
            return redirect(url_for('config'))
        return render_template('login.html', error='密码错误')
    return render_template('login.html')

# 配置页面路由
@app.route('/config', methods=['GET'])
@login_required
def config():
    return render_template('config.html')

# 更新配置接口
@app.route('/update_config', methods=['POST'])
@login_required
def update_config():
    try:
        global api_key, api_secret, is_logined, futures_api
        data = request.get_json()
        if not is_logined or api_key != data['api_key'] or api_secret != data['api_secret']:
            if data['api_key'] and data['api_secret']:
                api_key = data['api_key']
                api_secret = data['api_secret']
                environment = data['environment']
                host = "https://fx-api-testnet.gateio.ws/api/v4" if environment == 'TEST' else "https://fx-api.gateio.ws/api/v4"
                gate_config = Configuration(key=api_key, secret=api_secret, host=host)
                futures_api = FuturesApi(ApiClient(gate_config))
                account_res = futures_api.list_futures_accounts(SETTLE)
                if account_res:
                    set_position_mode(False)
                    get_symbol_tick_size()
                    is_logined = True
                    logger.info(f'登录成功')
            else:
                return jsonify({"status": "error", "message": "API key 或 secret 不能为空"})
        
        return jsonify({"status": "success", "message": "配置更新成功"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/reset_trading', methods=['GET'])
@login_required
def reset_trading():
    try:
        global trading_pairs, paused
        original_paused_state = paused
        
        # 如果策略正在运行，先暂停
        if not paused:
            paused = True
            time.sleep(2)  # 给一些时间让现有操作完成
            
        # 重置交易对信息
        trading_pairs = {}
        
        # 恢复原始暂停状态
        if not original_paused_state:
            paused = False
            
        logger.info('所有交易参数已重置')
        return jsonify({
            "status": "success", 
            "message": "所有交易参数已重置",
            "paused": paused
        })
    except Exception as e:
        logger.error(f'重置交易参数失败: {str(e)}')
        return jsonify({"status": "error", "message": str(e)})

@app.route('/get_trading_pairs', methods=['GET'])
@login_required
def get_trading_pairs():
    try:
        pairs_data = {}
        for symbol, trader in trading_pairs.items():
            pairs_data[symbol] = {
                'symbol': symbol,
                'zone_usdt': trader.zone_usdt,
                'loss_decrease': trader.current_loss_decrease,
                'direction': trader.direction,
                'position': trader.position,
                'mark_price': trader.mark_price,
                'entry_config': trader.entry_config,
                'exit_config': trader.exit_config,
                'pos_for_trail': trader.pos_for_trail,
                'trail_active_price': trader.trail_active_price,
                'trail_callback': trader.trail_callback,
                'up_line': trader.up_line,
                'down_line': trader.down_line,
                'entry_list': trader.entry_list,
                'exit_list': trader.exit_list,
                'paused': trader.paused
            }
            
        # 处理 API 和 Secret 的显示
        masked_api = f"{api_key[:3]}{'*' * (len(api_key)-3)}" if api_key else ""
        masked_secret = f"{api_secret[:3]}{'*' * (len(api_secret)-3)}" if api_secret else ""
        
        return jsonify({
            "status": "success", 
            "data": pairs_data,
            "paused": paused,
            "is_logined": is_logined,
            "api_key": masked_api,
            "api_secret": masked_secret
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/toggle_pause', methods=['GET'])
@login_required
def toggle_pause():
    try:
        global paused

        if not is_logined:
            return jsonify({"status": "error", "message": "请先登录"})
        paused = not paused
        return jsonify({
            "status": "success", 
            "message": "策略已暂停" if paused else "策略已启动",
            "paused": paused
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/toggle_symbol_pause/<symbol>', methods=['GET'])
@login_required
def toggle_symbol_pause(symbol):
    try:
        if not is_logined:
            return jsonify({"status": "error", "message": "请先登录"})
            
        if symbol not in trading_pairs:
            return jsonify({"status": "error", "message": f"交易对 {symbol} 不存在"})
            
        trader = trading_pairs[symbol]
        trader.paused = not trader.paused
        
        return jsonify({
            "status": "success", 
            "message": f"{symbol} 策略已{'暂停' if trader.paused else '启动'}",
            "paused": trader.paused
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/clean_symbol/<symbol>', methods=['GET'])
@login_required
def clean_symbol(symbol):
    try:
        if not is_logined:
            return jsonify({"status": "error", "message": "请先登录"})
            
        if symbol not in trading_pairs:
            return jsonify({"status": "error", "message": f"交易对 {symbol} 不存在"})
        
        # 平仓
        close_position(symbol)
        # 取消所有挂单
        cancel_all_orders(symbol)
        # 从trading_pairs中删除该交易对
        del trading_pairs[symbol]
        
        logger.info(f'{symbol} 清理完成')
        return jsonify({
            "status": "success", 
            "message": f"{symbol} 清理完成"
        })
    except Exception as e:
        logger.error(f'{symbol} 清理失败: {str(e)}')
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':

    # 启动Flask服务
    app.run(host='0.0.0.0', port=80)
