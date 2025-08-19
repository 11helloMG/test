from datetime import datetime
from config import Config

class Trader:
    def __init__(self):
        self.balance = Config.INITIAL_BALANCE
        self.positions = {}  # {symbol: quantity}
        self.trade_history = []  # 交易历史记录
        
        for symbol in Config.SYMBOLS:
            self.positions[symbol] = 0
    
    def calculate_commission(self, price, quantity):
        """计算交易手续费"""
        return price * quantity * Config.COMMISSION_RATE
    
    def calculate_slippage(self, price, quantity):
        """计算滑点成本"""
        return price * quantity * Config.SLIPPAGE_RATE
    
    def execute_order(self, symbol, action, price, quantity):
        """执行交易订单"""
        if quantity <= 0:
            return False
            
        commission = self.calculate_commission(price, quantity)
        slippage = self.calculate_slippage(price, quantity)
        total_cost = price * quantity + commission + slippage
        
        if action == 'BUY':
            if self.balance < total_cost:
                return False
            self.balance -= total_cost
            self.positions[symbol] += quantity
        elif action == 'SELL':
            if self.positions[symbol] < quantity:
                return False
            self.balance += (price * quantity - commission - slippage)
            self.positions[symbol] -= quantity
        else:
            return False
        
        # 记录交易
        self.trade_history.append({
            'timestamp': datetime.now(),
            'symbol': symbol,
            'action': action,
            'price': price,
            'quantity': quantity,
            'commission': commission,
            'slippage': slippage,
            'balance': self.balance
        })
        return True
    
    def get_position(self, symbol):
        """获取当前持仓"""
        return self.positions.get(symbol, 0)
    
    def get_balance(self):
        """获取当前资金"""
        return self.balance
    
    def get_trade_history(self):
        """获取交易历史"""
        return self.trade_history
