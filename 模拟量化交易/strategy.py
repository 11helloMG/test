from collections import deque
from config import Config

class DualMovingAverageStrategy:
    def __init__(self, symbol):
        self.symbol = symbol
        self.fast_window = Config.FAST_MA_PERIOD
        self.slow_window = Config.SLOW_MA_PERIOD
        self.price_history = deque(maxlen=self.slow_window)
        self.position = 0  # 当前持仓方向 (0: 无持仓, 1: 多头, -1: 空头)
        
    def update(self, price):
        """更新价格数据并计算信号"""
        self.price_history.append(price)
        
        if len(self.price_history) < self.slow_window:
            return None  # 数据不足
        
        # 计算快速均线
        fast_prices = list(self.price_history)[-self.fast_window:]
        fast_ma = sum(fast_prices) / len(fast_prices)
        
        # 计算慢速均线
        slow_ma = sum(self.price_history) / len(self.price_history)
        
        # 生成交易信号
        if fast_ma > slow_ma and self.position <= 0:
            self.position = 1
            return 'BUY'
        elif fast_ma < slow_ma and self.position >= 0:
            self.position = -1
            return 'SELL'
        return None
    
    def get_position(self):
        """获取当前持仓方向"""
        return self.position
