#!/bin/bash

# 查找并杀死运行中的trading_bot.py进程
echo "正在停止现有的trading_bot.py进程..."
pkill -f "python /data/tmp/gate_io_trading_bot/trading_bot.py"

# 等待进程完全终止
sleep 2

# 检查是否还有进程在运行
if pgrep -f "python /data/tmp/gate_io_trading_bot/trading_bot.py" > /dev/null; then
    echo "进程未能正常终止，强制杀死..."
    pkill -9 -f "python /data/tmp/gate_io_trading_bot/trading_bot.py"
    sleep 1
fi

# 进入项目目录
echo "进入项目目录..."
cd /data/tmp/gate_io_trading_bot || { echo "无法进入目录"; exit 1; }

# 拉取最新代码
echo "拉取最新代码..."
git pull || { echo "Git拉取失败"; exit 1; }

# 重新启动程序
echo "重新启动程序..."
nohup python /data/tmp/gate_io_trading_bot/trading_bot.py > /data/tmp/gate_io_trading_bot/bot.log 2>&1 &

# 检查是否成功启动
sleep 2
if pgrep -f "python /data/tmp/gate_io_trading_bot/trading_bot.py" > /dev/null; then
    echo "交易机器人已成功重启"
else
    echo "交易机器人启动失败"
    exit 1
fi

echo "重启过程完成"