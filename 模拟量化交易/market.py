import random
import time
from datetime import datetime
from config import Config

class MarketSimulator:
    def __init__(self):
        self.symbols = Config.SYMBOLS
        self.price_data = {}
        self.initialize_prices()
        
    def initialize_prices(self):
        """初始化各品种的价格"""
        base_prices = {
            'IF': 3800.0,  # 沪深300股指期货
            'IC': 6000.0,  # 中证500股指期货
            'IH': 2500.0   # 上证50股指期货
        }
        for symbol in self.symbols:
            self.price_data[symbol] = {
                'last_price': base_prices[symbol],
                'bid_price': base_prices[symbol] - 0.2,
                'ask_price': base_prices[symbol] + 0.2,
                'volume': 0,
                'time': datetime.now()
            }
    
    def generate_tick(self):
        """生成新的tick数据"""
        for symbol in self.symbols:
            last_price = self.price_data[symbol]['last_price']
            
            # 生成随机价格变动 (-0.5到+0.5之间)
            change = random.uniform(-0.5, 0.5)
            new_price = last_price + change
            
            # 更新市场数据
            self.price_data[symbol] = {
                'last_price': new_price,
                'bid_price': new_price - 0.2,
                'ask_price': new_price + 0.2,
                'volume': random.randint(1, 100),
                'time': datetime.now()
            }
        
        time.sleep(Config.DATA_INTERVAL)
        return self.price_data
    
    def get_current_data(self, symbol):
        """获取指定品种的当前市场数据"""
        return self.price_data.get(symbol, None)
