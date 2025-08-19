import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# 从Yahoo Finance下载数据
data = yf.download('AAPL', start='2024-01-01', end='2025-01-01')

# 创建DataFrame（只保留收盘价）
df = data[['Close']].copy()
df.columns = ['Close']

#止损比例
stop_loss_pct = 0.05

#计算指标
df['MA5'] = df['Close'].rolling(5).mean()
df['MA10'] = df['Close'].rolling(10).mean()

#初始化信号列
df['Signal'] = 0
df['Position'] = 0
df['Stop_Loss'] = np.nan

#生成信号
in_position = False
entry_price = 0

for i in range(10, len(df)):
    #金叉：短期均线上穿长期均线
    if df['MA5'].iloc[i] > df['MA10'].iloc[i] and df['MA5'].iloc[i-1] <= df['MA10'].iloc[i-1]:
        df['Signal'].iloc[i] = 1  # 买入信号
        if not in_position:
            in_position = True
            entry_price = df['Close'].iloc[i]
            #设置止损
            df['Stop_Loss'].iloc[i] = entry_price * (1 - stop_loss_pct)

    #死叉：短期均线下穿长期均线
    elif df['MA5'].iloc[i] < df['MA10'].iloc[i] and df['MA5'].iloc[i-1] >= df['MA10'].iloc[i-1]:
        df['Signal'].iloc[i] = -1  # 卖出信号
        if in_position:
            in_position = False
            df['Stop_Loss'].iloc[i] = np.nan

    #止损检查
    if in_position and df['Close'].iloc[i] < df['Stop_Loss'].iloc[i-1]:
        df['Signal'].iloc[i] = -2  # 止损信号
        in_position = False
        df['Stop_Loss'].iloc[i] = np.nan
    
    #跟踪止损
    if in_position:
        current_stop = df['Close'].iloc[i] * (1 - stop_loss_pct)
        df['Stop_Loss'].iloc[i] = max(current_stop, df['Stop_Loss'].iloc[i-1])
    
    #更新持仓状态
    df['Position'].iloc[i] = 1 if in_position else 0

# 可视化结果
plt.figure(figsize=(12, 8))

# 价格曲线
plt.plot(df['Close'], label='Price', alpha=0.5)
plt.plot(df['MA5'], label=f'{5}MA', color='orange')
plt.plot(df['MA10'], label=f'{10}MA', color='purple')

# 买卖信号
buy_signals = df[df['Signal'] > 0]
sell_signals = df[df['Signal'] < 0]
plt.scatter(buy_signals.index, buy_signals['Close'], 
            marker='^', color='r', s=100, label='Buy')
plt.scatter(sell_signals.index, sell_signals['Close'], 
            marker='v', color='g', s=100, label='Sell')

# 止损线
plt.plot(df['Stop_Loss'], label='Stop Loss', color='gray', linestyle='--', alpha=0.7)

plt.title('Trend Following Strategy')
plt.legend()
plt.grid(True)
plt.show()

# 打印交易统计
print(f"交易次数: {len(buy_signals) + len(sell_signals)}")
print(f"买入信号: {len(buy_signals)}次")
print(f"卖出信号: {len(sell_signals)}次 (包含止损)")