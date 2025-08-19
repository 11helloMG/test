# 模拟交易配置
class Config:
    # 初始资金
    INITIAL_BALANCE = 100000.0
    
    # 交易手续费率
    COMMISSION_RATE = 0.0002
    
    # 滑点率
    SLIPPAGE_RATE = 0.0001
    
    # 交易品种
    SYMBOLS = ['IF', 'IC', 'IH']  # 股指期货
    
    # 数据频率 (秒)
    DATA_INTERVAL = 5
    
    # 策略参数
    FAST_MA_PERIOD = 5   # 快速均线周期
    SLOW_MA_PERIOD = 20  # 慢速均线周期
