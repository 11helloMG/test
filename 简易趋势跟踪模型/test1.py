import pandas as pd
import numpy as np
import efinance as ef
import matplotlib.pyplot as plt

# 下载中股数据
stock_code = '002245'
data = ef.stock.get_quote_history(stock_code)
print(data.head())