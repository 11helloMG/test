import time
from market import MarketSimulator
from trader import Trader
from strategy import DualMovingAverageStrategy
from config import Config

def main():
    print("启动期货量化交易模拟系统...")
    
    # 初始化模块
    market = MarketSimulator()
    trader = Trader()
    strategies = {
        symbol: DualMovingAverageStrategy(symbol) 
        for symbol in Config.SYMBOLS
    }
    
    try:
        while True:
            # 获取市场数据
            tick_data = market.generate_tick()
            
            for symbol, data in tick_data.items():
                price = data['last_price']
                strategy = strategies[symbol]
                
                # 更新策略并获取信号
                signal = strategy.update(price)
                
                # 执行交易
                if signal:
                    quantity = 1  # 每次交易1手
                    print(f"{symbol} 信号: {signal} @ {price:.2f}")
                    if trader.execute_order(symbol, signal, price, quantity):
                        print(f"交易成功! 余额: {trader.get_balance():.2f}")
                    else:
                        print("交易失败: 资金或持仓不足")
                
                # 显示状态
                print(f"{symbol} 当前价: {price:.2f} | 持仓: {trader.get_position(symbol)}")
            
            print("-" * 40)
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n停止交易...")
        print("最终余额:", trader.get_balance())
        print("交易历史:")
        print(trader.get_trade_history())

if __name__ == "__main__":
    main()
